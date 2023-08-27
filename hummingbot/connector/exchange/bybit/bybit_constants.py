from hummingbot.core.api_throttler.data_types import LinkedLimitWeightPair, RateLimit
from hummingbot.core.data_type.in_flight_order import OrderState

DEFAULT_DOMAIN = "bybit_main"

HBOT_ORDER_ID_PREFIX = "BYBIT-"
MAX_ORDER_ID_LEN = 32
HBOT_BROKER_ID = "Hummingbot"

SIDE_BUY = "BUY"
SIDE_SELL = "SELL"

TIME_IN_FORCE_GTC = "GTC"
# Base URL
REST_URLS = {"bybit_main": "https://api.bybit.com",
             "bybit_testnet": "https://api-testnet.bybit.com"}

WSS_V1_PUBLIC_URL = {"bybit_main": "wss://stream.bybit.com/spot/quote/ws/v1",
                     "bybit_testnet": "wss://stream-testnet.bybit.com/spot/quote/ws/v1"}

WSS_PRIVATE_URL = {"bybit_main": "wss://stream.bybit.com/spot/ws",
                   "bybit_testnet": "wss://stream-testnet.bybit.com/spot/ws"}

# Websocket event types
DIFF_EVENT_TYPE = "diffDepth"
TRADE_EVENT_TYPE = "trade"
SNAPSHOT_EVENT_TYPE = "depth"

# Public API endpoints
LAST_TRADED_PRICE_PATH = "/spot/quote/v1/ticker/price"
EXCHANGE_INFO_PATH_URL = "/spot/v1/symbols"
SNAPSHOT_PATH_URL = "/spot/quote/v1/depth"
SERVER_TIME_PATH_URL = "/v5/market/time"

# Private API endpoints
ACCOUNTS_PATH_URL = "/spot/v1/account"
MY_TRADES_PATH_URL = "/spot/v1/myTrades"
ORDER_PATH_URL = "/spot/v1/order"

# Order States
ORDER_STATE = {
    "PENDING": OrderState.PENDING_CREATE,
    "NEW": OrderState.OPEN,
    "PARTIALLY_FILLED": OrderState.PARTIALLY_FILLED,
    "FILLED": OrderState.FILLED,
    "PENDING_CANCEL": OrderState.PENDING_CANCEL,
    "CANCELED": OrderState.CANCELED,
    "REJECTED": OrderState.FAILED,
}

WS_HEARTBEAT_TIME_INTERVAL = 30

# Rate Limit Type
SHARED_LIMIT = "SHARED"

# Rate Limit Max request
SHARED_MAX_REQUEST = 120
SPOT_DEFAULT_MAX_REQUEST = 20

# Rate Limit time intervals
ONE_SECOND = 1
FIVE_SECONDS = 5
ONE_MINUTES = 60

RATE_LIMITS = {
    # General
    # All HTTP Apis share 120/5s budget
    RateLimit(limit_id=SHARED_LIMIT, limit=SHARED_MAX_REQUEST, time_interval=FIVE_SECONDS),

    # Linked limits
    # TODO: fill in other API limits
    RateLimit(
        limit_id=SERVER_TIME_PATH_URL, limit=SPOT_DEFAULT_MAX_REQUEST, time_interval=ONE_SECOND,
        linked_limits=[LinkedLimitWeightPair(SHARED_LIMIT)],
    ),

}
