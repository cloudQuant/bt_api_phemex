from unittest.mock import AsyncMock
import pytest
from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_phemex.feeds.live_phemex.request_base import PhemexRequestData


async def test_phemex_async_request_allows_missing_extra_data(monkeypatch) -> None:
    request_data = PhemexRequestData(
        public_key="public-key",
        private_key="secret-key",
        exchange_name="PHEMEX___SPOT",
    )

    async_request_mock = AsyncMock(return_value={"code": 0, "data": {}})
    monkeypatch.setattr(request_data, "async_http_request", async_request_mock)

    result = await request_data.async_request("GET /public/time")

    assert isinstance(result, RequestData)
    assert result.get_extra_data() == {}
    assert result.get_input_data() == {"code": 0, "data": {}}
