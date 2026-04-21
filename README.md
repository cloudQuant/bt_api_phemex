# bt_api_phemex

Phemex exchange package for `bt_api`, supporting Spot trading.

## Features

- **Spot Trading**: Full REST API support for account, orders, market data
- **HMAC SHA256 Authentication**: Secure API key handling with expiry-based signatures
- **Hardcoded Configuration**: No YAML dependency — all exchange paths are defined in code

## Installation

```bash
pip install bt_api_phemex
```

Or install from source:

```bash
cd packages/bt_api_phemex
pip install -e .
```

## Quick Usage

```python
from bt_api_py import BtApi

api = BtApi(
    exchange_kwargs={
        "PHEMEX___SPOT": {
            "api_key": "your_api_key",
            "api_secret": "your_secret",
        }
    }
)

ticker = api.get_tick("PHEMEX___SPOT", "BTCUSDT")
print(ticker)
```

## Architecture

```
bt_api_phemex/
├── __init__.py
├── exchange_data/
│   └── __init__.py          # PhemexExchangeData, PhemexExchangeDataSpot
├── errors/
│   ├── __init__.py          # PhemexErrorTranslator (re-export)
│   └── phemex_translator.py # Error code mapping extending ErrorTranslator
├── tickers/
│   ├── __init__.py
│   └── phemex_ticker.py     # PhemexRequestTickerData
├── feeds/
│   └── live_phemex/
│       ├── __init__.py
│       ├── request_base.py   # PhemexRequestData (HMAC auth base)
│       └── spot.py           # PhemexRequestDataSpot
├── registry_registration.py  # Auto-registers with ExchangeRegistry
└── plugin.py                  # Plugin entrypoint for unified loading
```

## Dependencies

- `bt_api_base>=0.15,<1.0`
- Python 3.9+

## Supported Endpoints

| Method | Description |
|--------|-------------|
| `get_server_time` | Server time |
| `get_exchange_info` | Exchange symbols |
| `get_tick` / `get_ticker` | Query ticker data |
| `get_depth` | Order book depth |
| `get_kline` | K-line/candlestick data |
| `get_trade_history` | Recent trades |
| `get_balance` | Account balances |
| `get_account` | Account info |
| `make_order` | Place order |
| `cancel_order` | Cancel order |
| `query_order` | Query order status |
| `get_open_orders` | Get open orders |
