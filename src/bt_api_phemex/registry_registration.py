"""Phemex exchange auto-registration."""

try:
    from bt_api_base.balance_utils import simple_balance_handler as _phemex_balance_handler
except ImportError:
    _phemex_balance_handler = None

try:
    from bt_api_base.registry import ExchangeRegistry
except ImportError:
    ExchangeRegistry = None  # type: ignore

from bt_api_phemex.exchange_data import PhemexExchangeDataSpot
from bt_api_phemex.feeds.live_phemex import PhemexRequestDataSpot


def register_phemex():
    if ExchangeRegistry is None:
        return
    ExchangeRegistry.register_feed("PHEMEX___SPOT", PhemexRequestDataSpot)
    ExchangeRegistry.register_exchange_data("PHEMEX___SPOT", PhemexExchangeDataSpot)
    if _phemex_balance_handler is not None:
        ExchangeRegistry.register_balance_handler("PHEMEX___SPOT", _phemex_balance_handler)


register_phemex()
