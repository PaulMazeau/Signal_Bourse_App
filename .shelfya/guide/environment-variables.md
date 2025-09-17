# Environment Variables

## Overview
This document details the environment variables required for the operation of the trading bot modules in this repository. Environment variables are used to securely inject sensitive configuration such as API tokens and chat IDs, primarily for the Telegram messaging integration. Proper configuration of these variables is essential for successful communication and system operations.

## Key Features

- **Centralized Secrets Management**: Telegram bot tokens and chat IDs are managed via environment variables, enhancing security by decoupling sensitive data from source code.
- **Module-specific Scoping**: Different modules may use distinct environment variables to support separate Telegram bots or chat destinations.
- **Automatic Loading**: Uses `python-dotenv` to automatically load variables from a `.env` file for local development and deployment convenience.

## System Errors

- **Missing Environment Variable**:  
  *Description*: If a required environment variable is absent (e.g., `TELEGRAM_TOKEN`, `CHAT_ID`), Telegram notifications will fail silently and the system may not send crucial alerts.  
  *Resolution*: Ensure all required variables are defined in the `.env` file or system environment before launching the application.

- **Invalid Credentials**:  
  *Description*: Incorrect or expired tokens/chat IDs will result in message delivery failures to Telegram, which can be hard to detect without explicit error checks.  
  *Resolution*: Verify the tokens and chat IDs directly with Telegram and keep credentials updated.

## Usage Examples

**Example: `.env` file structure for single and multi-bot setups**

```env
# For Bot_RSI.py and Bot_RSI_MACD.py
TELEGRAM_TOKEN=123456:ABCDEF_TelegramBotToken
CHAT_ID=987654321

# For Bot_RSI_SP500.py (if using a dedicated bot/channel)
TELEGRAM_TOKEN_SP500=654321:ZYXWVU_AnotherBotToken
CHAT_ID_SP500=123498765

# Add further variables as needed for additional configurations
```

**How variables are accessed in Python code**
```python
import os
from dotenv import load_dotenv

load_dotenv() # Loads variables from `.env`

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
```

## System Integration

```
┌──────────────┐    ┌────────────────────────────┐    ┌─────────────┐
│  .env file   │───▶│   Bot Modules              │───▶│Telegram API │
│ (variables)  │    │ (e.g. Bot_RSI.py, ... )   │    │ (messaging) │
└──────────────┘    └────────────────────────────┘    └─────────────┘
        │                    │                            │
        ▼                    ▼                            ▼
[Defines tokens,      [Loads variables from         [Receives/broadcasts
chat IDs, ...]         .env, injects into code]     bot messages]
```

**Key Points:**
- The `.env` file supplies secret values.
- Each bot module auto-loads these using `python-dotenv` at runtime.
- Variables configure Telegram messaging, impacting notification delivery.
- Ensure correct variable mapping for each module to avoid misrouting alerts.