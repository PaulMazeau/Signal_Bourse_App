# Getting Started with Signal Bourse App

## Overview
The Signal Bourse App is a feature-rich toolkit designed to analyze, backtest, and notify users about stock trading signals based on common technical indicators. It focuses on leveraging the Relative Strength Index (RSI) and Moving Average Convergence Divergence (MACD) strategies for U.S. and European stocks, with special support for S&P 500 listings. The system enables both backtesting strategies on historical data and real-time monitoring with instant Telegram notifications, creating an integrated workflow for quantitative trading signal exploration.

## Key Features

- **Backtest RSI Strategy:** 
  - Simulate and evaluate RSI-based trading strategies on user-defined stocks.
  - Optimize stop-loss and take-profit parameters and report statistics like total return, win rate, and drawdown.
- **Backtest RSI + MACD Strategy:** 
  - Combine RSI and MACD signals to enhance buy/sell decision accuracy for selected stocks.
  - Automate strategy parameter sweeps for performance comparison.
- **S&P 500-Specific Tools:**
  - Retrieve the latest S&P 500 symbols automatically from the internet or from local cache.
  - Perform bulk backtests or real-time RSI-based signal generation across all S&P 500 components.
- **Automated Signal Notification:**
  - Monitor a set of stocks in real time and deliver trading signals (buy/sell suggestions) via Telegram bots, triggered by technical indicator thresholds.
- **Flexible Configuration:**
  - Easily modify target symbols, notification thresholds, and backtest windows.
- **Data Fetching & Integration:**
  - Seamless use of Yahoo! Finance (via yfinance) for historical and current price data.
  - Technical indicators handled by the `ta` package.

## System Errors

- **Data Fetching Errors (Yahoo! Finance):**
  - *Description:* API quota exceeded, network issues, or delisted tickers can lead to empty or incomplete data sets.
  - *Resolution:* Ensure symbols are current, retry with a slower request rate, or check internet connection.
- **Telegram Notification Failures:**
  - *Description:* Misconfiguration of bot tokens or chat IDs cause notification delivery errors.
  - *Resolution:* Verify `.env` tokens and chat IDs; confirm Telegram bot is set up and the chat exists.
- **Environment Variable Missing:**
  - *Description:* System fails to find necessary environment variables for notification or API access.
  - *Resolution:* Confirm `.env` file exists and includes `TELEGRAM_TOKEN`, `CHAT_ID`, and SP500 equivalents.
- **S&P 500 Symbol Fetch Issues:**
  - *Description:* Unable to access Wikipedia or local cache file missing.
  - *Resolution:* Check internet connection (for live fetching) or run the symbol cache script (`sp500_symbol.py`) to generate `sp500_symbols.json`.

## Usage Examples

```python
# Example 1: Backtest RSI strategy for a set of stocks
from BackTest_RSI import backtest_multiple_stocks
result, total, avg, max_dd, vol = backtest_multiple_stocks(
    ['AAPL', 'MSFT', 'GOOGL'],
    "2015-01-01", "2023-01-01",
    stop_loss=0.1,
    take_profit=0.2
)
print(result)  # Per-stock backtest metrics

# Example 2: Run combined RSI+MACD backtest
from BackTest_RSI_MACD import backtest_multiple_stocks
result, _, _, _, _ = backtest_multiple_stocks(
    ['AAPL', 'MSFT'],
    "2015-01-01", "2023-01-01",
    stop_loss=0.1,
    take_profit=0.15
)

# Example 3: Get the latest S&P 500 symbols and save to disk
from sp500_symbol import get_sp500_symbols, save_to_json
symbols = get_sp500_symbols()
save_to_json(symbols)

# Example 4: Monitor stocks in real-time and send alerts via Telegram
from Bot_RSI import monitor_rsi
monitor_rsi(['AAPL', 'GOOGL', 'MSFT'], threshold_low=28, threshold_high=72)

# Example 5: Run an S&P 500-wide signal notification
from Bot_RSI_SP500 import get_sp500_symbols_from_file, monitor_rsi_and_collect_data
sp500 = get_sp500_symbols_from_file()
for symbol in sp500:
    monitor_rsi_and_collect_data(symbol)
```

## System Integration

```
┌─────────────────────┐   ┌────────────────────┐   ┌──────────────────────┐
│ External Providers  │──▶│   Signal Bourse    │──▶│   User/Telegram App  │
│ (Yahoo! Finance,    │   │      Modules       │   │     Notification     │
│ Wikipedia, dotenv)  │   │ (Backtest, Bots,   │   │    & Reporting      │
│                     │   │  Symbol Utilities) │   │                      │
└─────────────────────┘   └────────────────────┘   └──────────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
[API data fetch, S&P 500]  [Backtest/Monitor logic]  [Human user, Telegram]
```

**Details:**
- *External Providers*: Yahoo! Finance for price data, Wikipedia or local `sp500_symbols.json` for S&P 500 symbols, Dotenv for secrets.
- *Signal Bourse Modules*: Core logic for backtests, indicator calculations, and Telegram bot triggers.
- *User/Telegram*: Consumption of trading signals via print output and Telegram instant messages.

---

*Begin by configuring your `.env` file, installing requirements, and using provided scripts to explore signal detection & backtesting workflows with your stocks of interest.*