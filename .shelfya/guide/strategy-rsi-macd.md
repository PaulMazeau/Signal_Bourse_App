# RSI-MACD Strategy Module

## Overview
The RSI-MACD Strategy module provides a robust analytics and alerting system based on the combined use of Relative Strength Index (RSI) and Moving Average Convergence Divergence (MACD) indicators. It enables users to **backtest multi-asset trading strategies** and **monitor live markets**, delivering buy/sell signals and system notifications via Telegram. The module supports both retrospective strategy evaluation and real-time signal generation, making it central for quantitative research and automated trading workflows.

## Key Features

- **Backtesting on Historical Data**: Run comprehensive backtests using RSI/MACD signals across multiple stocks, optimizing for profit targets and stop-loss thresholds. Evaluate performance through metrics like total return, win rate, drawdown, and volatility.
- **Signal Generation & Alerts**: Monitor live markets to detect precise buy/sell conditions based on configurable RSI and MACD values and send actionable signals via Telegram or console.
- **Multi-Asset Support**: Effortlessly analyze large stock baskets in both historical and real-time contexts.
- **Parameter Optimization**: Systematic search over ranges of stop-loss and take-profit parameters to identify optimal strategy settings.
- **External Messaging Integration**: Native support for Telegram API to automate signal broadcasting and alerting.

## System Errors

- **Data Download Failure**:  
  - *Description*: Failure to retrieve price history from Yahoo Finance (network issues, symbol error).  
  - *Resolution*: Ensure valid ticker symbols and network connectivity.
- **Indicator Calculation Error**:  
  - *Description*: Errors if price data is missing or contains NaN/inf values.  
  - *Resolution*: Check data integrity; handle preprocessing or missing data cases.
- **Telegram API Failure**:  
  - *Description*: Telegram message not sent (e.g., invalid token, chat ID, network).  
  - *Resolution*: Verify Telegram credentials and network. Test with known-good values.
- **Environment Variable Missing**:  
  - *Description*: TELEGRAM_TOKEN or CHAT_ID not loaded (not set in environment).  
  - *Resolution*: Create a `.env` file with correct variable declarations or export them in your environment.

## Usage Examples

```python
# 1. Run a backtest and optimize across multiple assets
from BackTest_RSI_MACD import backtest_multiple_stocks

tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
stop_loss = 0.10
take_profit = 0.15
start_date = "2020-01-01"
end_date = "2023-01-01"

results, total_ret, avg_ret, max_dd, avg_vol = backtest_multiple_stocks(
    tickers, start_date, end_date, stop_loss, take_profit
)
print(results)

# 2. Start live signal monitoring with Telegram alerts
from Bot_RSI_MACD import monitor_stocks

tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']  # Customize your list
monitor_stocks(tickers, threshold_low=30, threshold_high=70)
# If conditions are met, signals are printed and/or sent as Telegram messages

# 3. Customizing indicator parameters (advanced)
from Bot_RSI_MACD import get_indicators

rsi, macd_diff = get_indicators('AAPL', interval='1h', rsi_period=10, macd_short_period=8, macd_long_period=21)
print(f"RSI: {rsi}, MACD Diff: {macd_diff}")
```

## System Integration

```
┌─────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│ Market Data │─────▶│ RSI-MACD Strategy   │─────▶│ Users/Alert Systems │
│ (yfinance)  │      │   Module            │      │ (Telegram, Console) │
└─────────────┘      └─────────────────────┘      └─────────────────────┘
        │                    │                           │
        ▼                    ▼                           ▼
 [Stock Symbols]      [Backtesting Engine]       [Trader, Analyst, Bot]
                        [Live Monitor]
                        [Signal Generator]
                        [Optimization]
```

- **Dependencies**: `yfinance` (data), `ta` (indicators), `requests` (Telegram), `dotenv` (env), `threading`
- **This Module**: Central business logic for backtesting, alerting, indicator calculation, and parameter scanning
- **Used By**: Data science notebooks (research), automated trading scripts, Telegram alerting, end users wanting tactical entry/exit signals