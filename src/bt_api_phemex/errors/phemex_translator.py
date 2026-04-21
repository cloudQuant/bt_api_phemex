"""Phemex error translator."""

from __future__ import annotations

try:
    from bt_api_base.error import ErrorTranslator, UnifiedErrorCode
except ImportError:
    ErrorTranslator = object  # type: ignore
    UnifiedErrorCode = None  # type: ignore


class PhemexErrorTranslator(ErrorTranslator if ErrorTranslator != object else object):
    CODE_MAP = {
        "40001": UnifiedErrorCode.INVALID_API_KEY if UnifiedErrorCode else None,
        "40002": UnifiedErrorCode.INVALID_API_KEY if UnifiedErrorCode else None,
        "40003": UnifiedErrorCode.RATE_LIMIT_EXCEEDED if UnifiedErrorCode else None,
        "40004": UnifiedErrorCode.INVALID_SYMBOL if UnifiedErrorCode else None,
        "40005": UnifiedErrorCode.INVALID_ORDER if UnifiedErrorCode else None,
        "40006": UnifiedErrorCode.INSUFFICIENT_BALANCE if UnifiedErrorCode else None,
        "40007": UnifiedErrorCode.ORDER_NOT_FOUND if UnifiedErrorCode else None,
        "40008": UnifiedErrorCode.INVALID_PARAMETER if UnifiedErrorCode else None,
        "40100": UnifiedErrorCode.PERMISSION_DENIED if UnifiedErrorCode else None,
    }

    def translate(self, code: str | int, msg: str) -> tuple:
        key = str(code)
        mapped = self.CODE_MAP.get(key)
        if mapped is not None:
            return mapped, msg
        return super().translate(code, msg)
