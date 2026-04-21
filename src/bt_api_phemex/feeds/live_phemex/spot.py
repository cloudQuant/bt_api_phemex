"""Phemex Spot Feed."""

from __future__ import annotations

from typing import Any

try:
    from bt_api_base.logging_factory import get_logger
except ImportError:
    import logging

    def get_logger(name):
        return logging.getLogger(name)


try:
    from bt_api_phemex.exchange_data import PhemexExchangeDataSpot
except ImportError:
    PhemexExchangeDataSpot = None  # type: ignore

try:
    from bt_api_phemex.feeds.live_phemex.request_base import PhemexRequestData
except ImportError:
    PhemexRequestData = object  # type: ignore


class PhemexRequestDataSpot(PhemexRequestData):
    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.exchange_name = kwargs.get("exchange_name", "PHEMEX___SPOT")
        self.asset_type = kwargs.get("asset_type", "SPOT")
        self._params = kwargs.get("exchange_data", PhemexExchangeDataSpot())
        self.request_logger = get_logger("phemex_spot")

    def get_server_time(self, extra_data=None, **kwargs) -> Any:
        path, params, extra_data = self._get_server_time(extra_data=extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def get_exchange_info(self, extra_data=None, **kwargs) -> Any:
        path, params, extra_data = self._get_exchange_info(extra_data=extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def get_tick(self, symbol, extra_data=None, **kwargs) -> Any:
        path, params, extra_data = self._get_tick(symbol, extra_data=extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def get_ticker(self, symbol, extra_data=None, **kwargs) -> Any:
        return self.get_tick(symbol, extra_data=extra_data, **kwargs)

    def get_depth(self, symbol, count=20, extra_data=None, **kwargs) -> Any:
        path, params, extra_data = self._get_depth(
            symbol, size=count, extra_data=extra_data, **kwargs
        )
        return self.request(path, params=params, extra_data=extra_data)

    def get_kline(self, symbol, period="1h", count=100, extra_data=None, **kwargs) -> Any:
        path, params, extra_data = self._get_kline(
            symbol, period=period, count=count, extra_data=extra_data, **kwargs
        )
        return self.request(path, params=params, extra_data=extra_data)

    def get_trade_history(self, symbol, count=100, extra_data=None, **kwargs) -> Any:
        path, params, extra_data = self._get_trade_history(
            symbol, count=count, extra_data=extra_data, **kwargs
        )
        return self.request(path, params=params, extra_data=extra_data)

    def make_order(
        self, symbol, amount, price=None, order_type="buy-limit", extra_data=None, **kwargs
    ):
        path, params, extra_data = self._make_order(
            symbol, amount, price=price, order_type=order_type, extra_data=extra_data, **kwargs
        )
        return self.request(path, body=params, extra_data=extra_data, is_sign=True)

    def cancel_order(self, symbol=None, order_id=None, extra_data=None, **kwargs):
        path, params, extra_data = self._cancel_order(
            symbol=symbol, order_id=order_id, extra_data=extra_data, **kwargs
        )
        return self.request(path, params=params, extra_data=extra_data, is_sign=True)

    def query_order(self, symbol=None, order_id=None, extra_data=None, **kwargs):
        path, params, extra_data = self._query_order(
            symbol=symbol, order_id=order_id, extra_data=extra_data, **kwargs
        )
        return self.request(path, params=params, extra_data=extra_data, is_sign=True)

    def get_open_orders(self, symbol=None, extra_data=None, **kwargs) -> Any:
        path, params, extra_data = self._get_open_orders(
            symbol=symbol, extra_data=extra_data, **kwargs
        )
        return self.request(path, params=params, extra_data=extra_data, is_sign=True)

    def get_account(self, extra_data=None, **kwargs) -> Any:
        path, params, extra_data = self._get_account(extra_data=extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data, is_sign=True)

    def get_balance(self, extra_data=None, **kwargs) -> Any:
        path, params, extra_data = self._get_balance(extra_data=extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data, is_sign=True)

    def async_get_server_time(self, extra_data=None, **kwargs):
        path, params, extra_data = self._get_server_time(extra_data=extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data), self.async_callback
        )

    def async_get_exchange_info(self, extra_data=None, **kwargs):
        path, params, extra_data = self._get_exchange_info(extra_data=extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data), self.async_callback
        )

    def async_get_tick(self, symbol, extra_data=None, **kwargs):
        path, params, extra_data = self._get_tick(symbol, extra_data=extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data), self.async_callback
        )

    def async_get_depth(self, symbol, count=20, extra_data=None, **kwargs):
        path, params, extra_data = self._get_depth(
            symbol, size=count, extra_data=extra_data, **kwargs
        )
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data), self.async_callback
        )

    def async_get_kline(self, symbol, period="1h", count=100, extra_data=None, **kwargs):
        path, params, extra_data = self._get_kline(
            symbol, period=period, count=count, extra_data=extra_data, **kwargs
        )
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data), self.async_callback
        )

    def async_get_trade_history(self, symbol, count=100, extra_data=None, **kwargs):
        path, params, extra_data = self._get_trade_history(
            symbol, count=count, extra_data=extra_data, **kwargs
        )
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data), self.async_callback
        )

    def async_make_order(
        self, symbol, amount, price=None, order_type="buy-limit", extra_data=None, **kwargs
    ):
        path, params, extra_data = self._make_order(
            symbol, amount, price=price, order_type=order_type, extra_data=extra_data, **kwargs
        )
        self.submit(
            self.async_request(path, body=params, extra_data=extra_data, is_sign=True),
            self.async_callback,
        )

    def async_cancel_order(self, symbol=None, order_id=None, extra_data=None, **kwargs):
        path, params, extra_data = self._cancel_order(
            symbol=symbol, order_id=order_id, extra_data=extra_data, **kwargs
        )
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data, is_sign=True),
            self.async_callback,
        )

    def async_query_order(self, symbol=None, order_id=None, extra_data=None, **kwargs):
        path, params, extra_data = self._query_order(
            symbol=symbol, order_id=order_id, extra_data=extra_data, **kwargs
        )
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data, is_sign=True),
            self.async_callback,
        )

    def async_get_open_orders(self, symbol=None, extra_data=None, **kwargs):
        path, params, extra_data = self._get_open_orders(
            symbol=symbol, extra_data=extra_data, **kwargs
        )
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data, is_sign=True),
            self.async_callback,
        )

    def async_get_account(self, extra_data=None, **kwargs):
        path, params, extra_data = self._get_account(extra_data=extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data, is_sign=True),
            self.async_callback,
        )

    def async_get_balance(self, extra_data=None, **kwargs):
        path, params, extra_data = self._get_balance(extra_data=extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data, is_sign=True),
            self.async_callback,
        )
