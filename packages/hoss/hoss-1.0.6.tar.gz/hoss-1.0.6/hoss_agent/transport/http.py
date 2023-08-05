# -*- coding: utf-8 -*-

#  BSD 3-Clause License
#
#  Copyright (c) 2019, Elasticsearch BV
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
#  * Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import base64
import hashlib
import re
import ssl

import certifi
import urllib3
from urllib3.exceptions import MaxRetryError, TimeoutError

from hoss_agent.conf import constants
from hoss_agent.transport.base import TransportException
from hoss_agent.transport.http_base import AsyncHTTPTransportBase, HTTPTransportBase
from hoss_agent.utils import compat, json_encoder, read_pem_file
from hoss_agent.utils.logging import get_logger

logger = get_logger("hoss_agent.transport.http")


class Transport(HTTPTransportBase):
    def __init__(self, url, *args, **kwargs):
        super(Transport, self).__init__(url, *args, **kwargs)
        url_parts = compat.urlparse.urlparse(url)
        pool_kwargs = {"cert_reqs": "CERT_REQUIRED", "ca_certs": certifi.where(), "block": True}
        if self._server_cert and url_parts.scheme != "http":
            pool_kwargs.update(
                {"assert_fingerprint": self.cert_fingerprint, "assert_hostname": False, "cert_reqs": ssl.CERT_NONE}
            )
            del pool_kwargs["ca_certs"]
        elif not self._verify_server_cert and url_parts.scheme != "http":
            pool_kwargs["cert_reqs"] = ssl.CERT_NONE
            pool_kwargs["assert_hostname"] = False
        proxies = compat.getproxies_environment()
        proxy_url = proxies.get("https", proxies.get("http", None))
        if proxy_url and not compat.proxy_bypass_environment(url_parts.netloc):
            self.http = urllib3.ProxyManager(proxy_url, **pool_kwargs)
        else:
            self.http = urllib3.PoolManager(**pool_kwargs)

    def send(self, data):
        response = None
        headers = self._headers.copy() if self._headers else {}
        headers.update({"Authorization": "Bearer " + self.client.config.api_key})
        if compat.PY2 and isinstance(self._url, compat.text_type):
            url = self._url.encode("utf-8")
        else:
            url = self._url
        try:
            try:
                response = self.http.urlopen(
                    "POST", url, body=data, headers=headers, timeout=self._timeout
                )
                logger.debug("Sent request, url=%s size=%.2fkb status=%s", url, len(data) / 1024.0, response.status)
            except Exception as e:
                print_trace = True
                if isinstance(e, MaxRetryError) and isinstance(e.reason, TimeoutError):
                    message = "Connection to Ingress Server timed out " "(url: %s, timeout: %s seconds)" % (
                        self._url,
                        self._timeout,
                    )
                    print_trace = False
                else:
                    message = "Unable to reach Ingress Server: %s (url: %s)" % (e, self._url)
                raise TransportException(message, data, print_trace=print_trace)
            body = response.read()
            if response.status >= 400:
                if response.status == 429:  # rate-limited
                    message = "Temporarily rate limited: "
                    print_trace = False
                else:
                    message = "HTTP %s: " % response.status
                    print_trace = True
                message += body.decode("utf8", errors="replace")
                raise TransportException(message, data, print_trace=print_trace)
            return response.getheader("Location")
        finally:
            if response:
                response.close()

    def get_config(self, current_version=None):
        """
        Gets configuration from a remote APM Server

        :param current_version: version of the current configuration
        :return: a three-tuple of new version, config dictionary and validity in seconds.
                 Any element of the tuple can be None.
        """
        url = self._url
        data = json_encoder.dumps({
            "query": constants.AGENT_CONFIG_GRAPHQL_QUERY
        }).encode("utf-8")
        headers = self._headers.copy()
        headers.update(self.auth_headers)
        max_age = 10
        try:
            response = self.http.urlopen(
                "POST", url, body=data, headers=headers, timeout=self._timeout, preload_content=False
            )
        except (urllib3.exceptions.RequestError, urllib3.exceptions.HTTPError) as e:
            logger.debug("HTTP error while fetching remote config: %s", compat.text_type(e))
            return current_version, None, max_age
        body = response.read()
        if "Cache-Control" in response.headers:
            try:
                max_age = int(next(re.finditer(r"max-age=(\d+)", response.headers["Cache-Control"])).groups()[0])
            except StopIteration:
                logger.debug("Could not parse Cache-Control header: %s", response.headers["Cache-Control"])
        if response.status >= 400:
            return None, None, max_age

        if not body:
            logger.debug("AgentConfig query returns empty body and status code %s", response.status)
            return current_version, None, max_age

        json_body = json_encoder.loads(body.decode("utf-8"))
        if 'errors' in json_body:
            logger.debug("AgentConfig query returns errors %s", json_body['errors'][0]['message'])
            return current_version, None, max_age
        # graphql api isn't returning 304 yet. so do the check manually
        etag = response.headers.get("Etag")
        if current_version is not None and current_version == etag:
            # config is unchanged, return
            logger.debug("Configuration unchanged")
            return current_version, None, max_age

        config = parse_remote_config(json_body['data']['agentConfig'])
        return etag, config, max_age

    @property
    def cert_fingerprint(self):
        if self._server_cert:
            with open(self._server_cert, "rb") as f:
                cert_data = read_pem_file(f)
            digest = hashlib.sha256()
            digest.update(cert_data)
            return digest.hexdigest()
        return None

    @property
    def auth_headers(self):
        headers = super(Transport, self).auth_headers
        return {k.encode("ascii"): v.encode("ascii") for k, v in compat.iteritems(headers)}


class AsyncTransport(AsyncHTTPTransportBase, Transport):
    async_mode = True
    sync_transport = Transport


def parse_api_configuration(api):
    return {
        "uuid": api["uuid"],
        "hosts": api["hosts"],
        "sanitized_headers": api["configuration"]["sanitizedHeaders"],
        "sanitized_query_params": api["configuration"]["sanitizedQueryParams"],
        "sanitized_body_fields": api["configuration"]["sanitizedBodyFields"],
        "body_capture": api["configuration"]["bodyCapture"]
    }


def parse_remote_config(remote_config):
    apis = map(parse_api_configuration, remote_config['apis'])
    api_host_mapping = {h: a for a in apis for h in a["hosts"]}
    return {
        "account_api_configuration": {
            "uuid": remote_config["accountApiConfiguration"]["uuid"],
            "host_black_list": remote_config["accountApiConfiguration"]["hostBlacklist"],
            "sanitized_headers": remote_config["accountApiConfiguration"]["sanitizedHeaders"],
            "sanitized_query_params": remote_config["accountApiConfiguration"]["sanitizedQueryParams"],
            "sanitized_body_fields": remote_config["accountApiConfiguration"]["sanitizedBodyFields"],
            "body_capture": remote_config["accountApiConfiguration"]["bodyCapture"]
        },
        "apis": apis,
        "api_host_mapping": api_host_mapping
    }
