try:
    from bt_api_base.plugins.protocol import PluginInfo, PluginMetadata, PluginVersion
except ImportError:
    PluginInfo = None  # type: ignore
    PluginMetadata = None  # type: ignore
    PluginVersion = None  # type: ignore

from bt_api_phemex.exchange_data import PhemexExchangeDataSpot
from bt_api_phemex.feeds.live_phemex import PhemexRequestDataSpot


def _get_phemex_metadata():
    if PluginMetadata is None:
        return None
    return PluginMetadata(
        name="Phemex Exchange Plugin",
        version=PluginVersion(major=0, minor=1, patch=0),
        description="Phemex Spot trading support for bt_api_py",
        supported_exchanges=["PHEMEX___SPOT"],
        dependencies=["bt_api_base>=0.15,<1.0"],
    )


PHEMEX_PLUGIN_INFO = (
    PluginInfo(
        name="phemex",
        metadata=_get_phemex_metadata(),
        feed_class=PhemexRequestDataSpot,
        exchange_data_class=PhemexExchangeDataSpot,
    )
    if PluginInfo is not None
    else None
)
