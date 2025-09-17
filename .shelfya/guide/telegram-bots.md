# Telegram Bots Module

## Overview
The Telegram Bots module provides automated stock signal notifications directly to Telegram chats, leveraging technical indicators such as RSI and MACD. It consists of several bots focused on different strategies and asset universes (e.g., individual stocks, S&P 500 constituents). These bots retrieve market data, compute relevant indicators, assess buy/sell signals, and seamlessly send structured alerts to Telegram, thus facilitating timely, rules-based trading decisions and portfolio monitoring.

## Key Features

- **Automated RSI Alerts**: 
  - Monitors specified tickers' RSI values and sends buy/sell notifications to Telegram when RSI thresholds (overbought/oversold) are triggered.
  - Typical Use: Quick, rules-based momentum trading alerts.

- **Combined RSI & MACD Signal Alerts**:
  - Computes both RSI and MACD indicators, sending Telegram alerts only on "confluence" (e.g., RSI oversold AND MACD trending positive) to increase signal reliability.
  - Typical Use: More precise entries/exits based on multi-factor confirmation.

- **Bulk SP500 Scanning & Ranking**:
  - Loads the complete list of S&P 500 tickers from a JSON file, calculates RSI (and risk management parameters like stop loss/take profit) for each, and sends ranked signals to Telegram.
  - Typical Use: Systematic signal scanning across a wide equity universe for major market opportunities.

- **Multithreading for Efficient Parallel Monitoring**:
  - Each bot executes monitoring in parallel threads to ensure prompt, scalable data handling and minimal latency for live signals.

- **Telegram Integration**:
  - Easily configurable delivery of trading signals to designated Telegram chats using environment variables for tokens and chat IDs.
  - Typical Use: Hands-free, real-time notifications sent securely and instantly to any device.

## System Errors

- **Missing or Invalid Environment Variables**:
  - *Description*: If required tokens or chat IDs are not provided via environment variables, bots cannot send messages to Telegram.
  - *Resolution*: Ensure `.env` file includes correct `TELEGRAM_TOKEN`, `CHAT_ID`, and (for SP500) `TELEGRAM_TOKEN_SP500`, `CHAT_ID_SP500`.

- **Data Fetch Failures (Empty or Unreliable Ticker Data)**:
  - *Description*: When `yfinance` cannot retrieve sufficient data for a ticker (e.g., due to ticker delisting or network errors), signals may be skipped or output "data unavailable".
  - *Resolution*: Confirm ticker symbol accuracy, retry operation, check internet connection.

- **File Not Found Errors**:
  - *Description*: SP500 bulk scanning expects a file like `sp500_symbols.json` with ticker symbols.
  - *Resolution*: Place or properly reference the symbols file in the working directory.

- **Telegram API Request Failures**:
  - *Description*: If Telegram API requests fail (e.g., rate limits, network issues), messages may not be delivered.
  - *Resolution*: Check Telegram token validity, verify network access, respect API limits between sends.

## Usage Examples

**1. Basic RSI Alerts for Stock List**

```python
# Example: Monitor RSI for multiple tickers and send alerts to Telegram on signals

from Bot_RSI import monitor_rsi

tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
monitor_rsi(tickers)
```

**2. Multi-Factor (RSI + MACD) Alerts**

```python
# Example: Use combined RSI/MACD filter for signals

from Bot_RSI_MACD import monitor_stocks

tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
monitor_stocks(tickers)
```

**3. Full SP500 Scan and Ranked Alerts**

```python
# Example: Scan all SP500 tickers from file, send ranked RSI signals with SL/TP

from Bot_RSI_SP500 import get_sp500_symbols_from_file, monitor_rsi_and_collect_data, send_telegram_message

sp500_symbols = get_sp500_symbols_from_file('sp500_symbols.json')
for symbol in sp500_symbols:
    rsi_data = monitor_rsi_and_collect_data(symbol)
    for _, message in rsi_data:
        send_telegram_message(CHAT_ID, TELEGRAM_TOKEN, message)
```

## System Integration

```
┌─────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│  Data       │     │ Telegram Bots       │     │   User/Integrator   │
│  Sources    │────▶│  (RSI, MACD, SP500)│────▶│  (Telegram Chat)    │
│ (yfinance,  │     │                     │     │                     │
│  sp500_symbols.json)              │     │                     │
└─────────────┘     └─────────────────────┘     └─────────────────────┘
        │                     │                       │
        ▼                     ▼                       ▼
  [Market data,         [Signal processing,    [Receives messages,
   tickers list]         alert generation,      acts on alerts]
                         message dispatch]
```

**Integration Notes:**
- Module depends on up-to-date market data (via yfinance) and a valid ticks list (JSON for SP500 mode).
- Telegram bots must be registered with correct API keys and chat IDs (.env configuration).
- Alerts are delivered to any Telegram client with access to the configured chat.
- Easily adaptable for other tickers or strategies by modifying the tickers list or signal logic.