# RSI Strategy Module

## Overview
The RSI (Relative Strength Index) Strategy Module provides two core features: an automated trading signal bot and a historical backtesting framework, both based on RSI technical analysis. This module enables users to monitor live RSI conditions for multiple stocks (with alert notifications) and to optimize and evaluate RSI-based trading strategies across historical data, supporting informed decision-making for algorithmic traders or investors.

## Key Features
- **Live RSI Signal Bot**: Monitors selected tickers in real time, generating buy/sell signals using configurable RSI thresholds. Alerts can be sent automatically via Telegram, facilitating timely intervention.
- **Historical RSI Strategy Backtester**: Simulates trade outcomes based on RSI buy/sell signals, with configurable stop loss and take profit, over large date ranges and multiple assets. Returns metrics including total return, win rate, max drawdown, and volatility.
- **Batch Backtesting & Optimization**: Supports backtesting a basket of tickers over parameter grids, automatically generating portfolio performance statistics and visualizations.
- **Automated Telegram Notifications**: Seamless system integration for push notifications of critical events such as signal triggers.
- **Result Visualization**: Automatically saves graphs visualizing the simulated portfolio’s value over time for given backtest parameterizations.

## System Errors
- **Missing Environment Variables**: Failure to set `TELEGRAM_TOKEN` or `CHAT_ID` in the environment will prevent alert delivery.
  - *Resolution*: Ensure these values are present in your `.env` file and the file is loaded before the bot runs.
- **API Connectivity Issues**: Errors in downloading data from Yahoo Finance or sending Telegram notifications can occur due to network problems or changes in external services.
  - *Resolution*: Verify internet connectivity. If persistent, review API documentation or endpoints for updates.
- **Zero Trades Executed During Backtest**: Occurs if conditions never trigger a buy/sell within backtested data.
  - *Resolution*: Adjust threshold parameters to create more/fewer opportunities for trades.
- **Matplotlib Plot Rendering Issues**: Headless environments or missing dependencies may prevent chart saving.
  - *Resolution*: Install required plotting dependencies or run on a machine with a graphical backend.

## Usage Examples

```python
# Example: Live RSI Signal Monitoring with Telegram Integration
from Bot_RSI import monitor_rsi

# List of ticker symbols to monitor
ticker_symbols = ['AAPL', 'MSFT', 'GOOGL']
monitor_rsi(ticker_symbols, threshold_low=30, threshold_high=70)
```

```python
# Example: RSI Strategy Backtest on Single Stock
from BackTest_RSI import backtest_strategy

results, portfolio = backtest_strategy(
    ticker_symbol='AAPL',
    start_date='2019-01-01',
    end_date='2023-01-01',
    threshold_low=30,      # Buy if RSI < 30
    threshold_high=70,     # Sell if RSI > 70
    profit_target=0.10,    # Take profit at +10%
    stop_loss=0.05         # Stop loss at -5%
)
print(results)   # {'Total Return': ..., 'Win Rate': ..., ...}
```

```python
# Example: Batch Backtesting & Optimization Across Multiple Tickers
from BackTest_RSI import backtest_multiple_stocks

tickers = ['AAPL', 'MSFT', 'GOOGL']
results, total_return, average_return, max_drawdown, avg_volatility = \
    backtest_multiple_stocks(
        ticker_symbols=tickers,
        start_date='2010-01-01',
        end_date='2023-12-06',
        stop_loss=0.05,
        take_profit=0.10
    )
print(results)
```

## System Integration

```
┌──────────────────────┐    ┌───────────────────────┐    ┌─────────────────────────┐
│  Yahoo Finance API   │───▶│ RSI Strategy Module   │───▶│    User / Telegram Bot  │
│ (Real-time & histo)  │    │  (Bot_RSI,BackTest)   │    │  (Alert,Visualization)  │
└──────────────────────┘    └───────────────────────┘    └─────────────────────────┘
           │                      │                             │
           ▼                      ▼                             ▼
   [Market Data Feed]    [RSI Signal Calculation,           [Telegram API,
                             Backtest Simulation,         CLI, Plots, etc.]
                          Batch Optimization]
```
- **Dependencies**: Yahoo Finance, `ta` technical analysis library, Telegram API, matplotlib, dotenv.
- **Process**: Consumes market data to generate real-time signals and/or perform historical backtesting. Results trigger alerts or produce visual output.
- **Consumers**: End users (via CLI), Telegram messenger (via bot), system dashboards (via plot files).

**Use this module to integrate automated RSI-based signals and rigorous strategy evaluation directly into your trading workflow.**