# Signal Bourse Backtesting & Alert Modules

## Overview
This repository provides a feature set for building and analyzing stock trading strategies based on technical indicators (RSI, MACD) with coverage for individual stocks and the S&P500 index. It supports systematic backtesting over historical data, optimizing risk/reward parameters, and generating real-time trading alerts via Telegram bots.

These modules streamline quantitative strategy development and live monitoring by connecting data sources, analysis engines, and notification systems in a modular way.

## Key Features

- **RSI Backtesting**: Simulate and analyze trading strategies using the Relative Strength Index (RSI) over customizable historical periods, supporting risk (stop-loss) and reward (take-profit) optimization.
- **RSI + MACD Backtesting**: Enhance strategy realism by combining RSI and MACD indicators for buy/sell decisions, increasing signal reliability.
- **S&P500 Symbol Discovery**: Automatically fetch and store the complete list of S&P500 index symbols from the web, enabling broad portfolio-style testing.
- **Portfolio Simulation & Optimization**: Batch run strategies on configurable ticker lists; aggregate results, measure volatility, return, win rate, and drawdown, supporting parameter optimization and portfolio scaling.
- **RSI Alert Bot (All Stocks)**: Real-time bot that monitors chosen tickers, sending buy/sell signals via Telegram based on RSI thresholds.
- **RSI + MACD Alert Bot**: Live signal bot blends RSI and MACD for higher-confidence notifications, delivered to Telegram for actionable alerts.
- **RSI Alert Bot SP500**: Specialized monitoring for the S&P500 universe, sending slave/TP/SL signal info to Telegram, ranked by RSI intensity.
- **Configurable Integration**: All modules rely on public Yahoo Finance data, `ta` technical analysis library, and environment configuration for API keys and notification flows.

## System Errors

- **Data Download Failures**:  
  *Description*: Yahoo Finance or Wikipedia endpoints may be unreachable, leading to missing data or symbol lists.  
  *Resolution*: Ensure internet connection; check for endpoint changes; verify valid ticker symbols.

- **Empty Symbol List / JSON Errors**:  
  *Description*: S&P500 symbol fetching or file reading can fail or return empty.  
  *Resolution*: Re-run symbol grabber (`sp500_symbol.py`). Confirm the JSON file path/format.

- **Missing Environment Variables**:  
  *Description*: Telegram token/ID environment variables missing will break the bot notification process.  
  *Resolution*: Verify presence of `.env` file with correct `TELEGRAM_TOKEN` and `CHAT_ID` entries.

- **No Data for Given Period**:  
  *Description*: Backtest/date range may produce no data (e.g., holiday, delisted stock).  
  *Resolution*: Check ticker validity and adjust date range.

- **Rate Limiting/Overuse**:  
  *Description*: Excessive requests to APIs may be throttled, leading to missing notifications or partial results.  
  *Resolution*: Throttle bot actions or batch backtesting; increase `sleep` times between requests.

## Usage Examples

```python
# Backtesting an RSI-only strategy for multiple stocks
from BackTest_RSI import backtest_multiple_stocks
results, ttl_return, avg_return, max_dd, avg_vol = backtest_multiple_stocks(
    ['AAPL', 'GOOGL'], "2020-01-01", "2023-12-31", stop_loss=0.1, take_profit=0.2
)
print(results)

# Running live RSI+MACD alert bot (with .env properly set)
# Terminal: python Bot_RSI_MACD.py

# Getting and saving all S&P500 stock symbols to JSON
from sp500_symbol import save_to_json, get_sp500_symbols
symbols = get_sp500_symbols()
save_to_json(symbols)

# Running S&P500-wide RSI monitor and Telegram notifications (after symbols JSON created)
# Terminal: python Bot_RSI_SP500.py

# Example bot environment config (.env):
# TELEGRAM_TOKEN=your-telegram-token
# CHAT_ID=your-telegram-chat-id
```

## System Integration

```
┌──────────────────────┐   ┌─────────────────────┐   ┌──────────────────┐
│  Yahoo Finance (API) │─▶ │    Backtest/Alert   │─▶ │  Developer/User  │
│  Wikipedia (Symbols) │   │    Modules (.py)    │   │  Telegram Bot    │
└──────────────────────┘   └─────────────────────┘   └──────────────────┘
           │                      │                         │
           ▼                      ▼                         ▼
   [Data Source]         [Analysis, Simulation, Alert]   [Notification, Results]
         |                      |                         |
         └─────▶   S&P500 JSON  ◀────┘                   |
                          │                              |
                          ▼                              |
           [sp500_symbol.py: save/load]                  |
                          │                              ▼
                         [BackTest_RSI_SP500.py]    [Telegram Clients]
                         [Bot_RSI_SP500.py]
```

**Details:**
- **Dependencies**: Data comes from public Yahoo (prices, history), Wikipedia (S&P500 membership); requires user API tokens for Telegram alerts; `ta`, `yfinance`, `pandas`, `matplotlib` etc.
- **Process**: Backtest and alert modules orchestrate data pull, indicator calculation, simulation/decision logic, and message sending.
- **Consumers**: Outputs are plots, optimization tables, and/or live signal messages delivered to Telegram for human decision makers or for integration with further automation.