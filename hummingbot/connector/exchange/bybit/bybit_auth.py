import hashlib
import hmac
import json
import time
from collections import OrderedDict
from typing import Dict
from urllib.parse import urlencode

from hummingbot.connector.time_synchronizer import TimeSynchronizer
from hummingbot.core.web_assistant.auth import AuthBase
from hummingbot.core.web_assistant.connections.data_types import RESTMethod, RESTRequest, WSRequest


class BybitAuth(AuthBase):

    def __init__(self, api_key: str, secret_key: str, time_provider: TimeSynchronizer):
        self.api_key = api_key
        self.secret_key = secret_key
        self.recv_window = 5000
        self.time_provider = time_provider

    @staticmethod
    def keysort(dictionary: Dict[str, str]) -> Dict[str, str]:
        return OrderedDict(sorted(dictionary.items(), key=lambda t: t[0]))

    async def rest_authenticate(self, request: RESTRequest) -> RESTRequest:
        """
        Adds the server time and the signature to the request, required for authenticated interactions. It also adds
        the required parameter in the request header.
        :param request: the request to be configured for authenticated interaction
        """
        # Get payload
        if request.method == RESTMethod.POST:
            payload = json.dumps(request.data)
        else:
            payload = urlencode(request.params or {})

        # Update headers with authentication fields
        headers = self.add_auth_to_header(payload)
        if request.headers is not None:
            headers.update(request.headers)
        request.headers = headers

        return request

    async def ws_authenticate(self, request: WSRequest) -> WSRequest:
        """
        This method is intended to configure a websocket request to be authenticated. Bybit does not use this
        functionality
        """
        return request  # pass-through

    def add_auth_to_header(self, payload_str: str):
        timestamp = int(self.time_provider.time() * 1e3)

        # Generate signature
        params_str = str(timestamp) + self.api_key + str(self.recv_window) + payload_str
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            params_str.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        # Form headers
        headers = {
            'X-BAPI-TIMESTAMP': str(timestamp),
            'X-BAPI-API-KEY': self.api_key,
            'X-BAPI-RECV-WINDOW': str(self.recv_window),
            'X-BAPI-SIGN': signature,
        }

        return headers

    def generate_ws_authentication_message(self):
        """
        Generates the authentication message to start receiving messages from
        the private ws channels
        """
        # Generate expires
        expires = int((self.time_provider.time() + 10) * 1e3)

        # Generate signature
        _val = f'GET/realtime{expires}'
        signature = hmac.new(
            self.secret_key.encode("utf8"),
            _val.encode("utf8"),
            hashlib.sha256
        ).hexdigest()
        auth_message = {
            "op": "auth",
            "args": [self.api_key, expires, signature]
        }
        return auth_message

    def _time(self):
        return time.time()
