# Signal Bourse System Architecture

## Overview
The Signal Bourse system provides automated stock analysis, signal generation, and notification functionalities for equities based on technical indicators (such as RSI and MACD). The system offers capabilities for both **backtesting** trading strategies over historical data and **live monitoring** with automated notifications via Telegram. It supports multi-stock (including S&P 500) scenarios for both analysis and alerting, making it an automated and extensible toolkit for quantitative trading research and signal distribution.

## Key Features

- **Backtesting Engine (RSI & RSI+MACD):**
  Runs historical simulations across chosen tickers using technical indicator-based strategies (RSI, or RSI + MACD), supports parameter optimization (stop loss/take profit), and aggregates results for multi-asset portfolios. Useful for strategy evaluation and parameter tuning.

- **S&P 500 Symbol Handling:**
  Fetches and maintains the current list of S&P 500 stocks from Wikipedia, with export to JSON for consistent use in both backtesting and monitoring modules.

- **Live RSI-Based Signal Bot:**
  Continuously monitors equities using the RSI, issuing actionable buy/sell/hold messages for each monitored stock via Telegram. Provides immediate alerts on signal detection for user action.

- **Live RSI & MACD Signal Bot:**
  Combines RSI and MACD cross-detection for stronger signal accuracy, and sends buy/sell alerts through Telegram, reducing noise and improving entry/exit timing.

- **S&P 500-Wide Monitoring Bot:**
  Performs live RSI-based signal discovery across the entire S&P 500, ranking signals, and broadcasting the most notable opportunities to a dedicated Telegram channel, with individual threshold, stop loss, and take profit values.

## System Errors

- **Network/Data Source Failure:**
  If Yahoo Finance or Wikipedia is unavailable, symbol fetching, backtesting, and live monitoring may fail to retrieve data.
  - **Resolution:** Retry after some time; ensure a working internet connection; in live monitoring, empty or stale data triggers clear error messages.

- **Telegram API/Authentication Error:**
  Missing or incorrect Telegram bot credentials result in failure to deliver alert messages.
  - **Resolution:** Validate `.env` file settings for `TELEGRAM_TOKEN` and `CHAT_ID`; bot logs error if it cannot send the message.

- **File/JSON Symbol List Not Found:**
  S&P 500 monitoring bot depends on a `sp500_symbols.json` file; if missing, the module fails to process tickers.
  - **Resolution:** Regenerate the file using the symbol utility script; ensures centralized up-to-date symbol listing.

- **Empty Market Data:**
  For certain equities or market intervals, Yahoo Finance may not provide data, causing `NoneType` or empty data errors in some live bots.
  - **Resolution:** Bots log the unavailable symbol and skip it; no alerts are sent for missing data.

## Usage Examples

```python
# Backtest RSI strategy over a portfolio
from BackTest_RSI import backtest_multiple_stocks
results, total_return, avg_return, max_dd, avg_vol = backtest_multiple_stocks(
    ['AAPL', 'MSFT', 'GOOGL'], '2020-01-01', '2023-12-31', stop_loss=0.1, take_profit=0.15
)
print(results)

# Run RSI & MACD bot for live signals
# (requires proper .env setup for Telegram tokens and chat IDs)
from Bot_RSI_MACD import monitor_stocks
monitor_stocks(['AAPL', 'GOOGL'])

# Generate and save S&P 500 symbol list
from sp500_symbol import get_sp500_symbols, save_to_json
symbols = get_sp500_symbols()
save_to_json(symbols)

# Monitor RSI signals live for S&P 500 stocks and notify by Telegram
from Bot_RSI_SP500 import monitor_rsi_and_collect_data
# (Expects 'sp500_symbols.json' to exist)
rsi_data = monitor_rsi_and_collect_data('AAPL')  # Example for single ticker
```

## System Integration

```
┌────────────────────┐
│  Data Providers    │
│(Yahoo Finance, Wiki│
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐     ┌───────────────────┐
│ S&P 500 Symbol Util│     │   Backtest Engine │
│ (sp500_symbol.py)  │◄────┤ (BackTest_*)      │
└─────────┬──────────┘     └─────────┬─────────┘
          │                            │
   (JSON export)                 (Backtest Results)
          │                            │
          ▼                            ▼
┌──────────────────────┐       ┌─────────────────────┐
│   Live Signal Bots   │◄──────┤   CLI / User Output │
│(Bot_RSI_*, SP500)    │       │(Local / Telegram)   │
└─────────┬────────────┘       └─────────────────────┘
          │
          ▼
   [Telegram Channel]
```

- **Details:**  
  - Data Providers: Yahoo Finance for historical/real-time prices, Wikipedia for S&P 500 membership.
  - S&P 500 Symbol Util: Centralizes S&P 500 ticker access for use by backtesting and live bots via JSON file.
- **Process:**  
  - Backtest Engine: Applies strategies over historical data; iterates over tickers (from manual lists or S&P 500 JSON).
  - Live Signal Bots: Fetch live data, calculate indicators, and send alerts when conditions are met.
- **Consumers:**  
  - CLI output, local logs, or real-time Telegram notifications for traders, researchers, or automated trade triggers.