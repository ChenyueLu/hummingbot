from unittest import TestCase

from hummingbot.connector.exchange.bybit import bybit_constants as CONSTANTS, bybit_web_utils as web_utils


class WebUtilsTests(TestCase):
    def test_rest_url(self):
        url = web_utils.rest_url(path_url=CONSTANTS.TICKER_PATH_URL, domain=CONSTANTS.DEFAULT_DOMAIN)
        self.assertEqual('https://api.bybit.com/v5/market/tickers', url)
        url = web_utils.rest_url(path_url=CONSTANTS.TICKER_PATH_URL, domain='bybit_testnet')
        self.assertEqual('https://api-testnet.bybit.com/v5/market/tickers', url)
