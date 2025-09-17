# Backtesting Module

## Overview
The Backtesting module enables users to evaluate trading strategies based on technical indicators (such as RSI and MACD) against historical financial market data. It provides standardized interfaces for running backtests across single or multiple assets, optimizing strategy parameters, and generating key performance metrics. This module is essential for quantitatively validating trading ideas before live deployment.

## Key Features

- **RSI-Based Strategy Backtesting**: 
  - Backtests a buy/sell strategy using overbought (high) and oversold (low) RSI thresholds, profit targets, and stop-loss levels.
  - Evaluates performance across user-defined stocks or indices.
- **RSI + MACD Combined Backtesting**:
  - Tests strategies that require signals from both RSI and MACD indicators for entry and exit conditions.
  - Tailored for more advanced multi-indicator strategies.
- **SP500-Wide Backtesting**:
  - Automatically retrieves and backtests strategies across all S&P 500 components.
  - Facilitates large-scale analysis and benchmarking.
- **Parameter Optimization**:
  - Runs grid searches over ranges of stop-loss and profit-taking parameters.
  - Collects and summarizes performance metrics for comparison.
- **Performance Metrics Output**:
  - Reports total return, win rate, number of trades, max drawdown, and volatility for each asset and parameter set.
- **Portfolio Evolution Visualization** (RSI-based strategy):
  - Generates and saves plots showing cumulative portfolio value evolution over time for visual diagnostics.
  
## System Errors

- **Data Download Error**:
  - Description: Issues can arise when fetching historical data (e.g., incorrect ticker symbol, network outage, market holidays).
  - Resolution: Ensure internet connectivity, verify ticker symbols, and consider adding retry logic or validating with alternative data sources.
- **No Trade Executed**:
  - Description: For some assets or parameter sets, no trades may be executed due to restrictive thresholds or lack of signal.
  - Resolution: Adjust strategy thresholds, widen date range, or confirm the asset's trading activity within the timeframe.
- **Calculation/NaN Error in Indicator**:
  - Description: Technical indicator libraries can produce NaN values at series boundaries or if data is insufficient.
  - Resolution: Use adequate historical data and check for incomplete datasets. Preprocess data to fill/remove NaNs when necessary.
  
## Usage Examples

```python
from BackTest_RSI import backtest_strategy, backtest_multiple_stocks

# Single-asset RSI backtest
results, portfolio = backtest_strategy(
    ticker_symbol="AAPL",
    start_date="2015-01-01",
    end_date="2020-01-01",
    threshold_low=30,
    threshold_high=70,
    profit_target=0.15,
    stop_loss=0.1
)
print(results)

# Multi-asset RSI strategy optimization
tickers = ['AAPL', 'MSFT', 'GOOGL']
multi_results, total_ret, avg_ret, max_dd, avg_vol = backtest_multiple_stocks(
    ticker_symbols=tickers,
    start_date="2015-01-01",
    end_date="2020-01-01",
    stop_loss=0.1,
    take_profit=0.15
)
print(multi_results)

# RSI + MACD combined strategy
from BackTest_RSI_MACD import backtest_strategy as backtest_rsi_macd
metrics = backtest_rsi_macd(
    ticker_symbol='MSFT',
    start_date="2018-01-01",
    end_date="2021-01-01",
    rsi_threshold_low=30,
    rsi_threshold_high=70,
    macd_short=12,
    macd_long=26,
    macd_signal=9,
    profit_target=0.10,
    stop_loss=0.05
)
print(metrics)

# Backtesting across the S&P 500
from BackTest_RSI_SP500 import get_sp500_symbols, backtest_multiple_stocks

sp500 = get_sp500_symbols()
sp500_results, total_ret, avg_ret, max_dd, avg_vol = backtest_multiple_stocks(
    ticker_symbols=sp500,
    start_date="2020-01-01",
    end_date="2023-12-06",
    stop_loss=0.1,
    take_profit=0.2
)
print(sp500_results)
```

## System Integration

```
┌────────────────┐       ┌─────────────────────┐         ┌─────────────────────┐
│ Market Data    │──────▶│ Backtesting Module  │────────▶│ Analysis & Reports  │
│  (Yahoo/etc)   │       │ (RSI, MACD, SP500)  │         │  (User/UI/Plot)     │
└────────────────┘       └─────────────────────┘         └─────────────────────┘
         │                        │                               │
         ▼                        ▼                               ▼
  [Historical quotes]      [Run strategies, output metrics]    [Display/save results]
```
- **Dependencies**: Relies on market data sources (Yahoo Finance via `yfinance`), and technical analysis libraries (`ta`, `numpy`, `pandas`).
- **Process**: Fetches historical price data, computes indicators, iterates simulation, collects metrics.
- **Consumers**: Output feeds into dashboards, optimization pipelines, or further post-analysis by end users. Plots and reports are generated for interpretation and strategy refinement.