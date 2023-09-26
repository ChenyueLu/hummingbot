from hummingbot.core.api_throttler.data_types import LinkedLimitWeightPair, RateLimit
from hummingbot.core.data_type.in_flight_order import OrderState

DEFAULT_DOMAIN = "bybit_main"

HBOT_ORDER_ID_PREFIX = "BYBIT-"
MAX_ORDER_ID_LEN = 32
HBOT_BROKER_ID = "Hummingbot"

SIDE_BUY = "Buy"
SIDE_SELL = "Sell"

TIME_IN_FORCE_GTC = "GTC"
# Base URL
REST_URLS = {"bybit_main": "https://api.bybit.com",
             "bybit_testnet": "https://api-testnet.bybit.com"}

WSS_PUBLIC_URL = {"bybit_main": "wss://stream.bybit.com/v5/public/spot",
                  "bybit_testnet": "wss://stream-testnet.bybit.com/v5/public/spot"}

WSS_PRIVATE_URL = {"bybit_main": "wss://stream.bybit.com/v5/private",
                   "bybit_testnet": "wss://stream-testnet.bybit.com/v5/private"}

# Websocket public topics
WS_ORDERBOOK_TOPIC = "orderbook"
WS_TRADE_TOPIC = "publicTrade"

# Websocket private topics
WS_EXECUTION_TOPIC = "execution"
WS_WALLET_TOPIC = "wallet"
WS_ORDER_TOPIC = "order"

# Websocket event types
DIFF_EVENT_TYPE = "delta"
TRADE_EVENT_TYPE = "trade"
SNAPSHOT_EVENT_TYPE = "snapshot"

# Public API endpoints
TICKER_PATH_URL = "/v5/market/tickers"
INSTRUMENTS_INFO_PATH_URL = "/v5/market/instruments-info"
SNAPSHOT_PATH_URL = "/v5/market/orderbook"
SERVER_TIME_PATH_URL = "/v5/market/time"

# Private API endpoints
WALLET_BALANCE_PATH_URL = "/v5/account/wallet-balance"
EXECUTION_HISTORY_PATH_URL = "/v5/execution/list"
ORDER_PATH_URL = "/spot/v1/order"
ORDER_GET_PATH_URL = "/v5/order/realtime"
ORDER_CREATE_PATH_URL = "/v5/order/create"
ORDER_CANCEL_PATH_URL = "/v5/order/cancel"

# Order States
ORDER_STATE = {
    "Created": OrderState.PENDING_CREATE,
    "New": OrderState.OPEN,
    "PartiallyFilled": OrderState.PARTIALLY_FILLED,
    "Filled": OrderState.FILLED,
    "PartiallyFilledCanceled": OrderState.PENDING_CANCEL,
    "Cancelled": OrderState.CANCELED,
    "Rejected": OrderState.FAILED,
}

WS_HEARTBEAT_TIME_INTERVAL = 20

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
    # Public APIs
    RateLimit(
        limit_id=TICKER_PATH_URL, limit=SPOT_DEFAULT_MAX_REQUEST, time_interval=ONE_SECOND,
        linked_limits=[LinkedLimitWeightPair(SHARED_LIMIT)],
    ),
    RateLimit(
        limit_id=INSTRUMENTS_INFO_PATH_URL, limit=SPOT_DEFAULT_MAX_REQUEST, time_interval=ONE_SECOND,
        linked_limits=[LinkedLimitWeightPair(SHARED_LIMIT)],
    ),
    RateLimit(
        limit_id=SERVER_TIME_PATH_URL, limit=SPOT_DEFAULT_MAX_REQUEST, time_interval=ONE_SECOND,
        linked_limits=[LinkedLimitWeightPair(SHARED_LIMIT)],
    ),
    RateLimit(
        limit_id=SNAPSHOT_PATH_URL, limit=SPOT_DEFAULT_MAX_REQUEST, time_interval=ONE_SECOND,
        linked_limits=[LinkedLimitWeightPair(SHARED_LIMIT)],
    ),

    # Private APIs
    RateLimit(
        limit_id=WALLET_BALANCE_PATH_URL, limit=SPOT_DEFAULT_MAX_REQUEST, time_interval=ONE_SECOND,
        linked_limits=[LinkedLimitWeightPair(SHARED_LIMIT)],
    ),
    RateLimit(
        limit_id=EXECUTION_HISTORY_PATH_URL, limit=SPOT_DEFAULT_MAX_REQUEST, time_interval=ONE_SECOND,
        linked_limits=[LinkedLimitWeightPair(SHARED_LIMIT)],
    ),
    RateLimit(
        limit_id=ORDER_GET_PATH_URL, limit=SPOT_DEFAULT_MAX_REQUEST, time_interval=ONE_SECOND,
        linked_limits=[LinkedLimitWeightPair(SHARED_LIMIT)],
    ),
    RateLimit(
        limit_id=ORDER_CREATE_PATH_URL, limit=SPOT_DEFAULT_MAX_REQUEST, time_interval=ONE_SECOND,
        linked_limits=[LinkedLimitWeightPair(SHARED_LIMIT)],
    ),
    RateLimit(
        limit_id=ORDER_CANCEL_PATH_URL, limit=SPOT_DEFAULT_MAX_REQUEST, time_interval=ONE_SECOND,
        linked_limits=[LinkedLimitWeightPair(SHARED_LIMIT)],
    ),

}
