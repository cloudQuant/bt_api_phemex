"""Phemex ticker data containers."""

from __future__ import annotations

import time
from typing import Any

try:
    from bt_api_base.containers.tickers.ticker import TickerData
except ImportError:
    TickerData = object  # type: ignore

try:
    from bt_api_base.logging_factory import get_logger
except ImportError:
    import logging

    def get_logger(name):
        return logging.getLogger(name)


class PhemexRequestTickerData(TickerData if TickerData != object else object):
    SCALE = 1e8

    def __init__(
        self, data: dict[str, Any], symbol: str, asset_type: str, has_been_json_encoded=False
    ) -> None:
        super().__init__(data, has_been_json_encoded)
        self.symbol: str = symbol
        self.asset_type: str = asset_type
        self.last_price: float | None = None
        self.high_price: float | None = None
        self.low_price: float | None = None
        self.open_price: float | None = None
        self.volume_24h: float | None = None
        self.turnover_24h: float | None = None
        self.ask_price: float | None = None
        self.bid_price: float | None = None
        self.price_change: float | None = None
        self.price_change_percentage: float | None = None
        self.spread: float | None = None
        self.spread_percentage: float | None = None
        self.logger = get_logger("phemex_ticker")
        self._parse_data(data)

    def _parse_data(self, data: dict[str, Any]) -> None:
        try:
            result = data.get("data", {})
            self.symbol = result.get("symbol", self.symbol)
            self.exchange = "phemex"
            self.timestamp = data.get("timestamp", time.time())
            self.datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp))

            SCALE = self.SCALE
            VOLUME_SCALE = 1e8

            self.last_price = self._unscale(result.get("lastEp"), SCALE)
            self.high_price = self._unscale(result.get("highEp"), SCALE)
            self.low_price = self._unscale(result.get("lowEp"), SCALE)
            self.open_price = self._unscale(result.get("openEp"), SCALE)
            self.volume_24h = self._unscale(result.get("volumeEv"), VOLUME_SCALE)
            self.turnover_24h = self._unscale(result.get("turnoverEv"), SCALE)
            self.open_interest = result.get("openInterest")
            self.index_price = self._unscale(result.get("indexEp"), SCALE)
            self.mark_price = self._unscale(result.get("markEp"), SCALE)
            self.funding_rate = self._unscale(result.get("fundingRateEp"), 1e6)
            self.ask_price = self._unscale(result.get("askEp"), SCALE)
            self.bid_price = self._unscale(result.get("bidEp"), SCALE)

            if self.last_price is not None and self.open_price is not None:
                self.price_change = self.last_price - self.open_price
                self.price_change_percentage = (
                    (self.last_price - self.open_price) / self.open_price * 100
                    if self.open_price
                    else None
                )

            if self.ask_price is not None and self.bid_price is not None:
                self.spread = self.ask_price - self.bid_price
                self.spread_percentage = (
                    self.spread / self.bid_price * 100 if self.bid_price else None
                )

        except Exception as e:
            self.logger.error(f"Error parsing Phemex ticker data: {e}")

    def _unscale(self, value: int | None, scale: float) -> float | None:
        if value is None:
            return None
        return value / scale

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbol": self.symbol,
            "exchange": self.exchange,
            "timestamp": self.timestamp,
            "datetime": self.datetime,
            "last_price": self.last_price,
            "high_price": self.high_price,
            "low_price": self.low_price,
            "open_price": self.open_price,
            "volume_24h": self.volume_24h,
            "turnover_24h": self.turnover_24h,
            "ask_price": self.ask_price,
            "bid_price": self.bid_price,
            "spread": self.spread,
            "spread_percentage": self.spread_percentage,
            "price_change": self.price_change,
            "price_change_percentage": self.price_change_percentage,
            "asset_type": self.asset_type,
        }

    def validate(self) -> bool:
        if not self.symbol:
            return False
        if not self.last_price or self.last_price <= 0:
            return False
        return not (self.ask_price and self.bid_price and self.ask_price < self.bid_price)

    def __str__(self) -> str:
        pc = self.price_change_percentage if self.price_change_percentage is not None else 0
        return (
            f"PhemexTicker({self.symbol}: {self.last_price} "
            f"Bid:{self.bid_price} Ask:{self.ask_price} "
            f"Vol24h:{self.volume_24h} Chg:{pc:.2f}%)"
        )
