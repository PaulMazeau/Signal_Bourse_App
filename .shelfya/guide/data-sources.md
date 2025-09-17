# Data Sources

## Overview
The **Data Sources** module provides unified access to historical and real-time financial data for equities, focusing primarily on stocks and indices such as the S&P 500. This module powers backtesting, live monitoring, and trading signal evaluation functionalities. It enables the broader system to fetch, process, and maintain security symbols and price data, serving as a core foundation for all quantitative analysis and trading operations.

## Key Features

- **Symbol Retrieval**: 
  - Provides up-to-date lists of stock symbols for indices (e.g., full S&P 500 membership), enabling scalable and dynamic analysis across large asset universes.
- **Historical Price Download**: 
  - Fetches historical market data (open, high, low, close prices) for given stock symbols and time windows, supporting backtesting and research.
- **Technical Indicator Calculation**: 
  - Computes indicators such as RSI and MACD over historical and current prices, facilitating systematic trading strategies and automated analysis.
- **Live Data Access for Monitoring**: 
  - Supports real-time or most recent period data retrieval, enabling the system to generate live trading signals and send alerts.
- **Configurable Data Source Management**: 
  - Allows switching between different sets of security symbols (e.g., from local JSON or from updated web scrapes), supporting both static and up-to-date analyses.
- **Integration with Alerting/Notification Systems**: 
  - Exposes data and derived signals to downstream modules, particularly for communication channels such as Telegram bots.

## System Errors

- **Data Unavailable**: 
  - Occurs when market data cannot be retrieved (e.g., ticker not found, market closed, network issues).
    - **Resolution**: Ensure network connectivity, check symbol validity, and verify data provider (e.g., yfinance, pandas_datareader) is operational.
- **Empty Symbol List/File**: 
  - Triggered if symbol retrieval fails (e.g., Wikipedia page structure changes or file not found).
    - **Resolution**: Verify the online resource structure or local file existence and permissions.
- **Indicator Calculation Error**: 
  - Happens if price data is incomplete or has NaN values, causing technical indicator computation to fail.
    - **Resolution**: Ensure data completeness and clean/preprocess inputs; handle missing or invalid rows.
- **Environmental Configuration Missing**: 
  - Appears if required environment variables (e.g., API tokens, file paths) are not set.
    - **Resolution**: Provide necessary .env file or set variables in the host environment.

## Usage Examples

```python
# Retrieve list of S&P 500 symbols (dynamic from web)
from sp500_symbol import get_sp500_symbols
sp500_symbols = get_sp500_symbols()

# Save symbol list locally for later use
from sp500_symbol import save_to_json
save_to_json(sp500_symbols, filename="sp500_symbols.json")

# Load S&P 500 symbols from local file and retrieve latest RSI for each (used in Bot_RSI_SP500)
import json
with open("sp500_symbols.json", "r") as file:
    tickers = json.load(file)
# Example: fetch RSI for all symbols using Bot_RSI_SP500 logic
from ta.momentum import RSIIndicator
import yfinance as yf
for ticker in tickers[:3]:
    data = yf.download(ticker, period='1d')
    rsi = RSIIndicator(data['Close']).rsi().iloc[-1] if not data.empty else None
    print(f"{ticker}: RSI = {rsi}") 

# Backtest historical RSI strategy (used in BackTest_RSI)
from BackTest_RSI import backtest_strategy
results, _ = backtest_strategy('AAPL', '2020-01-01', '2023-12-31', 30, 70, 0.1, 0.1)
print(results)
```

## System Integration

```
┌──────────────────┐    ┌─────────────┐    ┌──────────────────────┐
│ External Sources │──▶│ Data Sources│──▶│ Quant/Strategy Layer  │
│ (yfinance, Web,  │   │ Module      │   │ (Backtest, Bots, etc.)│
│ Local Files, etc.)│   │             │   │                      │
└──────────────────┘    └─────────────┘    └──────────────────────┘
         │                     │                     │
         ▼                     ▼                     ▼
 [S&P 500 scrape,      [Symbol list mgmt,     [Backtesting, live 
  .json file read,      price/indicator        signal generation, 
  yfinance queries]     calculation, data      notification
                        pre-processing]        dispatch]
```

- **Dependencies**:
  - `yfinance` for price data.
  - Wikipedia (via `pandas.read_html`) for dynamic symbol list.
  - Local JSON files as symbol caches.
- **This Module**:
  - Fetches, stores, and serves securities symbols and price/indicator data.
- **Used By/Consumers**:
  - Backtesting engines (e.g., BackTest_RSI, BackTest_RSI_MACD).
  - Algorithmic bots (e.g., Bot_RSI, Bot_RSI_MACD, Bot_RSI_SP500).
  - Notification modules (for sending trading signals).