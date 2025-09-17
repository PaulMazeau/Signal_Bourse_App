# S&P 500 RSI Strategy Module

## Overview
The S&P 500 RSI Strategy Module provides a feature set for backtesting, live monitoring, and notification of trading signals based on the Relative Strength Index (RSI) on S&P 500 stocks. It enables data-driven traders and developers to conduct systematic research and real-time tracking of RSI-based strategies, focusing on the S&P 500 universe. The module integrates with data sources (Yahoo Finance), messaging platforms (Telegram), and provides reusable functions for symbol management.

## Key Features

- **S&P 500 Symbol Retrieval & Management**:  
  - Fetches up-to-date symbols directly from Wikipedia or loads cached symbols from JSON for reliability and speed.  
  - Supports saving and loading of the S&P 500 constituent list.

- **RSI Signal Generation & Notification**:  
  - Calculates current RSI values for each stock.  
  - Detects buy (RSI low) and sell (RSI high) signals.  
  - Sends formatted signals and trade parameters (stop-loss, take-profit) to Telegram channels.

- **Strategy Backtesting Across S&P 500**:  
  - Runs historical backtests for each symbol using specified RSI thresholds, profit targets, and stop loss.  
  - Aggregates metrics across all tested stocks, including return, win rate, drawdown, and volatility.

- **Batch Analysis & Optimization**:  
  - Supports parameter sweeps for profit targets and stop-loss levels.  
  - Outputs comparative results for strategy optimization.

- **Thread-Safe Data Collection**:  
  - Ensures that concurrent data downloads and calculations are safe for batch processing.

## System Errors

- **Data Download Failure**:  
  Description: Fails to retrieve data for a ticker, possibly due to symbol delisting or API issues.  
  Resolution: Check the symbol’s validity and internet connection; consider updating the S&P 500 list.

- **RSI Calculation Error**:  
  Description: Data required to compute RSI is missing or insufficient historical data.  
  Resolution: Ensure the ticker has enough historical data and retry. Skip tickers with empty datasets.

- **Telegram Notification Failure**:  
  Description: Message not sent due to invalid token or network error.  
  Resolution: Verify Telegram token and chat ID environment variables. Retry on connection issues.

## Usage Examples

```python
# Retrieve and save the latest S&P 500 symbols (offline mode)
from sp500_symbol import get_sp500_symbols, save_to_json
symbols = get_sp500_symbols()
save_to_json(symbols)

# Run backtest over the S&P 500
from BackTest_RSI_SP500 import backtest_multiple_stocks
results, total_return, avg_return, max_dd, avg_vol = backtest_multiple_stocks(
    symbols, "2020-01-01", "2023-12-06", stop_loss=0.1, take_profit=0.2
)
print(results)

# Live RSI monitoring and Telegram notification
from Bot_RSI_SP500 import monitor_rsi_and_collect_data, send_telegram_message
data = monitor_rsi_and_collect_data('AAPL')
for _, message in data:
    send_telegram_message(chat_id='123456', token='TOKEN', message=message)
```

## System Integration

```
┌────────────────┐          ┌──────────────────────┐      ┌──────────────────┐
│  Data Sources  │ ───────▶ │  S&P 500 RSI Module  │ ────▶│ User & Automation│
│ (Yahoo Finance,│          │   (this repository)  │      │(Telegram, Output)│
│  Wikipedia)    │          │                      │      │                  │
└────────────────┘          └──────────────────────┘      └──────────────────┘
         │                           │                           │
         ▼                           ▼                           ▼
- Live/Hist Stock Data       - RSI Calculation           - Telegram Signaling
- S&P 500 Table             - Strategy Backtest         - Batch Reporting
                            - Optimization Loop         - Strategy Analytics
                            - Load/Save Symbols         - Trading Decisions
```
**Details:**  
- Fetches symbols and market data from external sources.  
- Integrates RSI analytics for both historical (backtest) and real-time scanning.  
- Communicates actionable signals and batch results via messaging or direct output, enabling seamless workflow automation or user monitoring.