import yfinance as yf
import ta
import threading
import requests
import os
from dotenv import load_dotenv
import time
import json

load_dotenv()  # Charge les variables d'environnement

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN_SP500')
CHAT_ID = os.getenv('CHAT_ID_SP500')
lock = threading.Lock()

def send_telegram_message(chat_id, token, message):
    base_url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(base_url)

def get_rsi(ticker_symbol, interval='1d', period=14):
    with lock:
        stock_data = yf.download(ticker_symbol, interval=interval)
    if stock_data.empty:
        return None 
    rsi = ta.momentum.RSIIndicator(stock_data['Close'], window=period).rsi()
    return round(rsi.iloc[-1], 1) if not rsi.empty else None

def monitor_rsi_and_collect_data(ticker_symbol, threshold_low=30, threshold_high=70):
    rsi_data = []
    rsi = get_rsi(ticker_symbol)
    if rsi is None:
        print(f"Données non disponibles pour {ticker_symbol}")
        return rsi_data

    with lock:
        stock_data = yf.download(ticker_symbol, period='1d')
    current_price = stock_data['Close'].iloc[-1]

    stop_loss = current_price * 0.90 
    take_profit = current_price * 1.20 

    if rsi < threshold_low or rsi > threshold_high:
        message = f'{ticker_symbol}: {"Achat" if rsi < threshold_low else "Vente"}, RSI = {rsi}, SL = {round(stop_loss, 2)}, TP = {round(take_profit, 2)}'
        rsi_data.append((rsi, message))

    return rsi_data
    

def get_sp500_symbols_from_file(filename="sp500_symbols.json"):
    with open(filename, 'r') as file:
        symbols = json.load(file)
    return symbols

if __name__ == '__main__':
    sp500_symbols = get_sp500_symbols_from_file()
    all_rsi_data = []

    for ticker in sp500_symbols:
        rsi_data = monitor_rsi_and_collect_data(ticker)
        all_rsi_data.extend(rsi_data)

    sorted_rsi_data = sorted(all_rsi_data, key=lambda x: x[0], reverse=True)

    for _, message in sorted_rsi_data:
        send_telegram_message(CHAT_ID, TELEGRAM_TOKEN, message)
        time.sleep(1) 
