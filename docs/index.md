# PHEMEX Documentation

## English

Welcome to the PHEMEX documentation for bt_api.

### Quick Start

```bash
pip install bt_api_phemex
```

```python
from bt_api_phemex import PhemexApi
feed = PhemexApi(api_key="your_key", secret="your_secret")
ticker = feed.get_ticker("BTCUSDT")
```

## 中文

欢迎使用 bt_api 的 PHEMEX 文档。

### 快速开始

```bash
pip install bt_api_phemex
```

```python
from bt_api_phemex import PhemexApi
feed = PhemexApi(api_key="your_key", secret="your_secret")
ticker = feed.get_ticker("BTCUSDT")
```

## API Reference

See source code in `src/bt_api_phemex/` for detailed API documentation.
