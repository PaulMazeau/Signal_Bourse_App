import yfinance as yf
import ta
import threading
import requests
import os
from dotenv import load_dotenv
import pandas as pd
import time

load_dotenv()  # Charge les variables d'environnement

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
lock = threading.Lock()

def send_telegram_message(chat_id, token, message):
    base_url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(base_url)

def get_rsi(ticker_symbol, interval='1d', period=14):
    with lock:
        stock_data = yf.download(ticker_symbol, interval=interval)
    if stock_data.empty:
        return None  # Gérer le cas où les données ne sont pas disponibles
    rsi = ta.momentum.RSIIndicator(stock_data['Close'], window=period).rsi()
    return round(rsi.iloc[-1], 1) if not rsi.empty else None

def monitor_rsi_and_collect_data(ticker_symbol, threshold_low=30, threshold_high=70):
    rsi_data = []
    rsi = get_rsi(ticker_symbol)
    if rsi is None:
        print(f"Données non disponibles pour {ticker_symbol}")
        return rsi_data  # Continuer avec le symbole suivant si les données ne sont pas disponibles

    with lock:
        stock_data = yf.download(ticker_symbol, period='1d')
        print('DONE')
    current_price = stock_data['Close'].iloc[-1]

    # Calculer le stop loss et le take profit
    stop_loss = current_price * 0.90  # 10% en dessous du prix actuel
    take_profit = current_price * 1.20  # 20% au-dessus du prix actuel

    if rsi < threshold_low or rsi > threshold_high:
        message = f'{ticker_symbol}: {"Achat" if rsi < threshold_low else "Vente"}, RSI = {rsi}, SL = {round(stop_loss, 2)}, TP = {round(take_profit, 2)}'
        rsi_data.append((rsi, message))

    return rsi_data

def get_sp500_symbols():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url, verify=False)
    tables = pd.read_html(response.content, header=0)
    sp500_table = tables[0]
    sp500_symbols = sp500_table['Symbol'].tolist()
    return sp500_symbols

if __name__ == '__main__':
    sp500_symbols = get_sp500_symbols()
    all_rsi_data = []

    for ticker in sp500_symbols:
        rsi_data = monitor_rsi_and_collect_data(ticker)
        all_rsi_data.extend(rsi_data)

    # Trier les données RSI en ordre décroissant
    sorted_rsi_data = sorted(all_rsi_data, key=lambda x: x[0], reverse=True)

    # Envoyer les messages Telegram pour les actions triées, avec un délai de 10 secondes entre chaque envoi
    for _, message in sorted_rsi_data:
        send_telegram_message(CHAT_ID, TELEGRAM_TOKEN, message)
        time.sleep(10)  # Attendre 10 secondes avant d'envoyer le prochain message
