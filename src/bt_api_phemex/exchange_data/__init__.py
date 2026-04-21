"""Phemex exchange data configuration - hardcoded defaults, no YAML."""

from __future__ import annotations

from typing import Any

try:
    from bt_api_base.exchanges.exchange_data import ExchangeData
except ImportError:
    ExchangeData = object  # type: ignore


class PhemexExchangeData(ExchangeData):
    USDT_PRICE_SCALE = 1e8
    BTC_PRICE_SCALE = 1e8
    USD_PRICE_SCALE = 1e8

    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "phemex"
        self.rest_url = "https://api.phemex.com"
        self.wss_url = "wss://ws.phemex.com"
        self.rest_paths: dict[str, str] = {}
        self.wss_paths: dict[str, Any] = {}

        self.kline_periods = {
            "1m": "60",
            "5m": "300",
            "15m": "900",
            "30m": "1800",
            "1h": "3600",
            "4h": "14400",
            "1d": "86400",
            "1w": "604800",
        }
        self.reverse_kline_periods = {v: k for k, v in self.kline_periods.items()}
        self.legal_currency = ["USDT", "USD", "BTC", "ETH"]

    def get_symbol(self, symbol: str) -> str:
        symbol = symbol.replace("/", "")
        if symbol.startswith("s") and not symbol.startswith("SOL"):
            return symbol
        if self.asset_type == "SPOT":
            return f"s{symbol}"
        return symbol

    def get_period(self, period: str) -> str:
        return self.kline_periods.get(period, period)

    def get_rest_path(self, request_type: str, **kwargs: Any) -> str:
        if request_type not in self.rest_paths or self.rest_paths[request_type] == "":
            raise ValueError(
                f"REST path not found for key: {request_type} on exchange {self.exchange_name}"
            )
        return self.rest_paths[request_type]

    def get_wss_path(self, **kwargs) -> str:
        import json

        key = kwargs.get("topic", "")
        if "symbol" in kwargs:
            kwargs["symbol"] = self.get_symbol(kwargs["symbol"])
        if "period" in kwargs:
            kwargs["period"] = self.get_period(kwargs["period"])

        if key not in self.wss_paths or self.wss_paths[key] == "":
            raise ValueError(f"WSS path not found for key: {key} on exchange {self.exchange_name}")
        req = self.wss_paths[key].copy()
        req_key = list(req.keys())[0]
        for k, v in kwargs.items():
            if isinstance(v, str):
                req[req_key] = [req[req_key][0].replace(f"<{k}>", v)]

        return json.dumps(req)

    def scale_price(self, price, scale=None):
        if scale is None:
            scale = self.USDT_PRICE_SCALE
        return int(price * scale)

    def unscale_price(self, scaled_price, scale=None):
        if scale is None:
            scale = self.USDT_PRICE_SCALE
        return scaled_price / scale


class PhemexExchangeDataSpot(PhemexExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.asset_type = "SPOT"
        self.exchange_name = "PHEMEX___SPOT"
        self.rest_url = "https://api.phemex.com"
        self.wss_url = "wss://ws.phemex.com"

        self.rest_paths = {
            "get_server_time": "GET /exchange/public/md/v2/timestamp",
            "get_exchange_info": "GET /public/products",
            "get_tick": "GET /md/spot/ticker/24hr",
            "get_depth": "GET /md/v2/orderbook",
            "get_kline": "GET /md/v2/kline",
            "get_trades": "GET /md/v2/trade",
            "get_account": "GET /spot/wallets",
            "get_balance": "GET /spot/wallets",
            "make_order": "POST /spot/orders/create",
            "cancel_order": "DELETE /spot/orders",
            "query_order": "GET /spot/orders/active",
            "get_open_orders": "GET /spot/orders/active",
        }

        self.wss_paths = {}

    def get_symbol(self, symbol: str) -> str:
        symbol = symbol.replace("/", "")
        if symbol.startswith("s") and not symbol.startswith("SOL"):
            return symbol
        return f"s{symbol}"
