import yfinance as yf
import ta
import numpy as np
import pandas as pd

def backtest_strategy(ticker_symbol, start_date, end_date, rsi_threshold_low, rsi_threshold_high, macd_short, macd_long, macd_signal, profit_target, stop_loss):
    # Télécharger les données historiques
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
    
    # Calculer le RSI et le MACD
    rsi = ta.momentum.RSIIndicator(stock_data['Close']).rsi()
    macd = ta.trend.MACD(stock_data['Close'], window_slow=macd_long, window_fast=macd_short, window_sign=macd_signal)

    # Initialiser les variables pour le backtest
    in_position = False
    entry_price = 0
    trades = []
    peak = -np.inf
    max_drawdown = 0
    portfolio_values = [0]  # Commencer avec la valeur du portefeuille à 0

    # Itérer sur les données pour simuler les transactions
    for date, row in stock_data.iterrows():
        current_price = row['Close']
        current_rsi = rsi.loc[date]
        macd_diff = macd.macd_diff().loc[date]

        if not in_position and current_rsi < rsi_threshold_low and macd_diff > 0:
            # Achat
            in_position = True
            entry_price = current_price
        elif in_position:
            # Calculer la perte actuelle en pourcentage
            current_loss = (entry_price - current_price) / entry_price

            if current_rsi > rsi_threshold_high or macd_diff < 0 or (current_price >= entry_price * (1 + profit_target)) or (current_loss >= stop_loss):
                # Vente ou Stop-Loss
                in_position = False
                exit_price = current_price if current_loss < stop_loss else entry_price * (1 - stop_loss)
                profit = (exit_price - entry_price) / entry_price
                trades.append(profit)

                # Mettre à jour la valeur du portefeuille
                current_portfolio_value = sum(trades)
                portfolio_values.append(current_portfolio_value)

                # Mettre à jour le pic et le drawdown maximal
                peak = max(peak, current_portfolio_value)
                drawdown = (peak - current_portfolio_value) / peak
                max_drawdown = max(max_drawdown, drawdown)

    # Calculer la volatilité des retours
    returns = np.diff(portfolio_values)
    volatility = np.std(returns) if len(returns) > 0 else 0

    # Calculer les métriques de performance
    total_return = sum(trades)
    win_rate = len([t for t in trades if t > 0]) / len(trades) if trades else 0

    return {
        "Total Return": total_return,
        "Win Rate": win_rate,
        "Number of Trades": len(trades),
        "Max Drawdown": max_drawdown,
        "Volatility": volatility
    }

def backtest_multiple_stocks(ticker_symbols, start_date, end_date, stop_loss, take_profit):
    results = {}
    total_return_cumulative = 0
    max_drawdown_cumulative = 0
    volatility_cumulative = 0

    # Paramètres MACD
    macd_short = 12
    macd_long = 26
    macd_signal = 9

    for ticker_symbol in ticker_symbols:
        # Inclure les paramètres MACD dans l'appel de la fonction
        result = backtest_strategy(ticker_symbol, start_date, end_date, 30, 70, macd_short, macd_long, macd_signal, take_profit, stop_loss)
        results[ticker_symbol] = result
        total_return_cumulative += result["Total Return"]
        max_drawdown_cumulative = max(max_drawdown_cumulative, result["Max Drawdown"])
        volatility_cumulative += result["Volatility"]

    average_return = total_return_cumulative / len(ticker_symbols)
    average_volatility = volatility_cumulative / len(ticker_symbols)

    return results, total_return_cumulative, average_return, max_drawdown_cumulative, average_volatility


# Plages de paramètres pour l'optimisation
stop_loss_range = [0.05, 0.1, 0.15]
take_profit_range = [0.05, 0.1, 0.15, 0.2]

# Stockage des résultats d'optimisation
optimization_results = []

# Liste des symboles boursiers à tester
ticker_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', '^FCHI', '^GSPC']

for stop_loss in stop_loss_range:
    for take_profit in take_profit_range:
        backtest_result, total_return, average_return, max_drawdown, average_volatility = backtest_multiple_stocks(ticker_symbols, "2010-01-01", "2023-12-06", stop_loss, take_profit)
        
        optimization_results.append({
            "Stop Loss": stop_loss,
            "Take Profit": take_profit,
            "Total Return": total_return,
            "Average Return": average_return,
            "Max Drawdown": max_drawdown,
            "Average Volatility": average_volatility,
            "Results": backtest_result
        })

# Afficher les résultats d'optimisation
for result in optimization_results:
    print(f"Stop Loss: {result['Stop Loss']}, Take Profit: {result['Take Profit']}, Total Return: {result['Total Return']}, Average Return: {result['Average Return']}, Max Drawdown: {result['Max Drawdown']}, Average Volatility: {result['Average Volatility']}")