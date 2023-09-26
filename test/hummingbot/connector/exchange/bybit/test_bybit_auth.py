import asyncio
import hashlib
import hmac
import json
from typing import Awaitable, Dict, Mapping, Optional
from unittest import TestCase
from unittest.mock import MagicMock
from urllib.parse import urlencode

from hummingbot.connector.exchange.bybit.bybit_auth import BybitAuth
from hummingbot.core.web_assistant.connections.data_types import RESTMethod, RESTRequest, WSJSONRequest


class BybitAuthTests(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.api_key = "testApiKey"
        self.secret_key = "testSecretKey"

        self.mock_time_provider = MagicMock()
        self.mock_time_provider.time.return_value = 1000

        self.auth = BybitAuth(
            api_key=self.api_key,
            secret_key=self.secret_key,
            time_provider=self.mock_time_provider,
        )

    def async_run_with_timeout(self, coroutine: Awaitable, timeout: int = 1):
        ret = asyncio.get_event_loop().run_until_complete(asyncio.wait_for(coroutine, timeout))
        return ret

    def test_add_auth_params_to_get_request_without_params(self):
        request = RESTRequest(
            method=RESTMethod.GET,
            url="https://test.url/api/endpoint",
            is_auth_required=True,
            throttler_limit_id="/api/endpoint"
        )
        headers_expected = self._headers_expected(RESTMethod.GET, request.params)

        self.async_run_with_timeout(self.auth.rest_authenticate(request))

        self.assertEqual(headers_expected['X-BAPI-API-KEY'], request.headers["X-BAPI-API-KEY"])
        self.assertEqual(headers_expected['X-BAPI-TIMESTAMP'], request.headers["X-BAPI-TIMESTAMP"])
        self.assertEqual(headers_expected['X-BAPI-RECV-WINDOW'], request.headers["X-BAPI-RECV-WINDOW"])
        self.assertEqual(headers_expected['X-BAPI-SIGN'], request.headers['X-BAPI-SIGN'])

    def test_add_auth_params_to_get_request_with_params(self):
        params = {
            "param_z": "value_param_z",
            "param_a": "value_param_a"
        }
        request = RESTRequest(
            method=RESTMethod.GET,
            url="https://test.url/api/endpoint",
            params=params,
            is_auth_required=True,
            throttler_limit_id="/api/endpoint"
        )

        headers_expected = self._headers_expected(RESTMethod.GET, request.params)

        self.async_run_with_timeout(self.auth.rest_authenticate(request))

        self.assertEqual(headers_expected['X-BAPI-API-KEY'], request.headers["X-BAPI-API-KEY"])
        self.assertEqual(headers_expected['X-BAPI-TIMESTAMP'], request.headers["X-BAPI-TIMESTAMP"])
        self.assertEqual(headers_expected['X-BAPI-RECV-WINDOW'], request.headers["X-BAPI-RECV-WINDOW"])
        self.assertEqual(headers_expected['X-BAPI-SIGN'], request.headers['X-BAPI-SIGN'])

    def test_add_auth_params_to_post_request(self):
        params = {"param_z": "value_param_z", "param_a": "value_param_a"}
        request = RESTRequest(
            method=RESTMethod.POST,
            url="https://test.url/api/endpoint",
            data=json.dumps(params),
            is_auth_required=True,
            throttler_limit_id="/api/endpoint"
        )
        headers_expected = self._headers_expected(RESTMethod.POST, request.data)

        self.async_run_with_timeout(self.auth.rest_authenticate(request))

        self.assertEqual(headers_expected['X-BAPI-API-KEY'], request.headers["X-BAPI-API-KEY"])
        self.assertEqual(headers_expected['X-BAPI-TIMESTAMP'], request.headers["X-BAPI-TIMESTAMP"])
        self.assertEqual(headers_expected['X-BAPI-RECV-WINDOW'], request.headers["X-BAPI-RECV-WINDOW"])
        self.assertEqual(headers_expected['X-BAPI-SIGN'], request.headers['X-BAPI-SIGN'])

    def test_no_auth_added_to_ws_request(self):
        payload = {"param1": "value_param_1"}
        request = WSJSONRequest(payload=payload, is_auth_required=True)
        self.async_run_with_timeout(self.auth.ws_authenticate(request))
        self.assertEqual(payload, request.payload)

    def test_ws_auth_message(self):
        auth_message = self.auth.generate_ws_authentication_message()
        expected_auth_message = self._ws_auth_message_expected()

        self.assertEqual(expected_auth_message, auth_message)

    def _generate_signature(self, payload_str: str) -> str:
        param_str = str(1000000) + self.api_key + str(5000) + payload_str
        digest = hmac.new(
            self.secret_key.encode("utf8"),
            param_str.encode("utf8"),
            hashlib.sha256
        ).hexdigest()
        return digest

    def _headers_expected(
            self,
            request_method: RESTMethod,
            request_params: Optional[Mapping[str, str]],
    ) -> Dict:
        request_params = request_params if request_params else {}

        if request_method == RESTMethod.GET:
            payload_str = urlencode(request_params)
        else:
            payload_str = request_params

        headers = {}

        signature = self._generate_signature(payload_str)

        # headers need to verify
        headers["X-BAPI-API-KEY"] = self.api_key
        headers["X-BAPI-TIMESTAMP"] = "1000000"
        headers["X-BAPI-RECV-WINDOW"] = "5000"
        headers["X-BAPI-SIGN"] = signature

        return headers

    def _ws_auth_message_expected(self):
        expires = 1010000

        signature = str(hmac.new(
            bytes(self.secret_key, "utf-8"),
            bytes(f"GET/realtime{expires}", "utf-8"), digestmod="sha256"
        ).hexdigest())

        expected = {
            "op": "auth",
            "args": [self.api_key, expires, signature]
        }

        return expected
