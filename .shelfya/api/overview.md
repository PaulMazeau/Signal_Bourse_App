# Signal Bourse App: API & System Overview

## Overview
The Signal Bourse App provides a collection of modules for automated stock market analysis, backtesting, and signal broadcasting. It focuses on technical indicators (RSI, MACD) to generate buy/sell signals, optimize trading strategies, and notify users via Telegram. The system supports batch backtesting across multiple tickers (including S&P 500), real-time monitoring, and integration with external data providers. It is built for algorithmic traders and analysts seeking actionable signals and strategy validation.

## Key Features

- **RSI-based Backtesting:**  
  Simulate trading results using RSI threshold-based strategies over historical data. Supports multiple stocks and parameter optimization to evaluate strategy performance across scenarios.

- **RSI+MACD Backtesting:**  
  Enhance signal accuracy by combining RSI and MACD crossovers. Run automated backtests on provided stock tickers with comprehensive performance metrics output.

- **S&P 500 Symbol Management:**  
  Automatically fetches and maintains the list of current S&P 500 tickers for use in batch analysis, ensuring up-to-date coverage of US large-cap equities.

- **Telegram Signal Bots:**  
  Monitor selected stocks in real-time (based on RSI or RSI+MACD) and send actionable buy/sell signals to users via the Telegram messaging API—supporting both arbitrary tickers and the entire S&P 500.

- **Parameter Grid Optimization:**  
  Automate the search for best stop-loss and take-profit parameters by running strategies across multiple combinations and reporting aggregate/cumulative results.

- **Portfolio Metrics Aggregation:**  
  For each strategy and configuration, calculate and report overall return, win rate, drawdown, trade count, and volatility, facilitating performance comparison.

## System Errors

- **Data Unavailability:**  
  *Description:* Historical or real-time market data may be missing or incomplete (often from yfinance or Pandas read errors).  
  *Resolution:* Ensure the ticker symbol is valid; check internet connection and API rate limits; retry or skip symbols with missing data.

- **Telegram API Failure:**  
  *Description:* Signal messages may fail to send due to invalid token, incorrect chat ID, or network interruptions.  
  *Resolution:* Verify environment variables (`TELEGRAM_TOKEN`, `CHAT_ID`) in your `.env` file; check Telegram Bot permissions; handle failed requests gracefully by logging or retrying.

- **File Access/Write Error (S&P 500 Symbols):**  
  *Description:* Issues while reading or writing `sp500_symbols.json` file.  
  *Resolution:* Check file permissions; ensure the working directory exists and is writable.

- **Strategy Parameter Issues:**  
  *Description:* Invalid or extreme values for thresholds, stop-loss, or take-profit may lead to empty trades or poor results.  
  *Resolution:* Validate input parameters; use recommended ranges (`30/70` for RSI, standard MACD configuration).

## Usage Examples

```python
# Backtest RSI strategy across multiple stocks
from BackTest_RSI import backtest_multiple_stocks
results, total_return, avg_return, max_dd, avg_vol = backtest_multiple_stocks(
    ticker_symbols=['AAPL', 'MSFT', 'GOOGL'],
    start_date="2015-01-01",
    end_date="2020-01-01",
    stop_loss=0.1,
    take_profit=0.2
)

# Monitor tickers with RSI-based Telegram notifications
from Bot_RSI import monitor_rsi
monitor_rsi(['AAPL', 'GOOGL', 'AMZN'], threshold_low=30, threshold_high=70)

# Run S&P 500 signal bot (requires 'sp500_symbols.json')
from Bot_RSI_SP500 import monitor_rsi_and_collect_data
sp500_symbols = ['MSFT', 'AAPL', 'AMZN']
for ticker in sp500_symbols:
    monitor_rsi_and_collect_data(ticker)

# Fetch S&P 500 symbol list and save as JSON
from sp500_symbol import get_sp500_symbols, save_to_json
symbols = get_sp500_symbols()
save_to_json(symbols)
```

## System Integration

```
┌─────────────────────┐     ┌──────────────────────┐     ┌─────────────────────────────┐
│ External Data Feeds │ ───▶│  BackTest Modules    │ ───▶│  Users / Analyst / Bots     │
│  (Yahoo Finance,    │     │ - RSI, RSI+MACD      │     │ - CLI, Telegram             │
│   Wikipedia, etc.)  │     │ - S&P500 Batch, etc. │     │ - Result Visualization      │
└─────────────────────┘     └──────────────────────┘     └─────────────────────────────┘
           │                      │                              │
           ▼                      ▼                              ▼
  [Market Data]        [Backtesting & Signal Processing]     [Notifications, Reports,
                                                                Data Export]
           │                      │                              │
           └──────────────────────┴──────────────────────────────┘
                                  │
                                  ▼
                    ┌──────────────────────────────┐
                    │   Telegram API Integration   │
                    └──────────────────────────────┘
```

**Details:**
- **Dependencies:**  
  - Yahoo Finance (price data), Wikipedia (list of S&P 500)
  - Python packages: `yfinance`, `ta`, `pandas`, `matplotlib`, `requests`, `dotenv`, etc.

- **Process:**  
  - Fetch/prepare symbol lists → Download historical or real-time prices → Compute indicators (RSI, MACD) → Run backtests and optimizations → Generate signals/metrics → Notify or report.

- **Consumers:**  
  - Human users via CLI outputs, Telegram messages
  - Downstream automation (bots, dashboards, further analytics tools)  
