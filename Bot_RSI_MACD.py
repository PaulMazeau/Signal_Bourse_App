import yfinance as yf
import ta
import threading
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
lock = threading.Lock()

def send_telegram_message(chat_id, token, message):
    base_url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(base_url)

def get_indicators(ticker_symbol, interval='1d', rsi_period=14, macd_short_period=12, macd_long_period=26, macd_signal=9):
    with lock:
        stock_data = yf.download(ticker_symbol, interval=interval)
    rsi = ta.momentum.RSIIndicator(stock_data['Close'], window=rsi_period).rsi()
    macd = ta.trend.MACD(stock_data['Close'], window_slow=macd_long_period, window_fast=macd_short_period, window_sign=macd_signal)
    
    return rsi.iloc[-1], macd.macd_diff().iloc[-1]

def monitor_stocks(ticker_symbols, threshold_low=30, threshold_high=70):
    for ticker_symbol in ticker_symbols:
        rsi, macd_diff = get_indicators(ticker_symbol)
        if rsi < threshold_low and macd_diff > 0:
            message = f'{ticker_symbol}: Strong Buy Signal, RSI = {rsi}, MACD Increasing'
            send_telegram_message(CHAT_ID, TELEGRAM_TOKEN, message)
        elif rsi > threshold_high and macd_diff < 0:
            message = f'{ticker_symbol}: Strong Sell Signal, RSI = {rsi}, MACD Decreasing'
            send_telegram_message(CHAT_ID, TELEGRAM_TOKEN, message)
        else:
            print(f'{ticker_symbol}: No Clear Signal. RSI: {rsi}, MACD Diff: {macd_diff}')

if __name__ == '__main__':
    ticker_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
    for ticker in ticker_symbols:
        thread = threading.Thread(target=monitor_stocks, args=([ticker],))
        thread.start()
        thread.join()
