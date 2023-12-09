import yfinance as yf
import ta
import numpy as np
import pandas as pd

def get_sp500_symbols():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tables = pd.read_html(url, header=0)
    sp500_table = tables[0]
    sp500_symbols = sp500_table['Symbol'].tolist()
    return sp500_symbols

def backtest_strategy(ticker_symbol, start_date, end_date, threshold_low, threshold_high, profit_target, stop_loss):
    # Télécharger les données historiques
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
    
    # Calculer le RSI
    rsi = ta.momentum.RSIIndicator(stock_data['Close']).rsi()

    # Initialiser les variables pour le backtest
    in_position = False
    entry_price = 0
    trades = []
    peak = -np.inf
    max_drawdown = 0
    portfolio_values = [0]

    # Itérer sur les données pour simuler les transactions
    for date, row in stock_data.iterrows():
        current_price = row['Close']
        current_rsi = rsi.loc[date]

        if not in_position and current_rsi < threshold_low:
            in_position = True
            entry_price = current_price
        elif in_position:
            current_loss = (entry_price - current_price) / entry_price

            if current_rsi > threshold_high or (current_price >= entry_price * (1 + profit_target)) or (current_loss >= stop_loss):
                in_position = False
                exit_price = current_price if current_loss < stop_loss else entry_price * (1 - stop_loss)
                profit = (exit_price - entry_price) / entry_price
                trades.append(profit)

                current_portfolio_value = sum(trades)
                portfolio_values.append(current_portfolio_value)

                peak = max(peak, current_portfolio_value)
                drawdown = (peak - current_portfolio_value) / peak
                max_drawdown = max(max_drawdown, drawdown)

    returns = np.diff(portfolio_values)
    volatility = np.std(returns) if len(returns) > 0 else 0

    total_return = sum(trades)
    win_rate = len([t for t in trades if t > 0]) / len(trades) if trades else 0
    volatility = np.std(np.diff(portfolio_values)) if len(portfolio_values) > 1 else 0

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

    for ticker_symbol in ticker_symbols:
        result = backtest_strategy(ticker_symbol, start_date, end_date, 30, 80, take_profit, stop_loss)
        results[ticker_symbol] = result

        total_return_cumulative += result["Total Return"]
        max_drawdown_cumulative = max(max_drawdown_cumulative, result["Max Drawdown"])
        volatility_cumulative += result["Volatility"]

    average_return = total_return_cumulative / len(ticker_symbols)
    average_volatility = volatility_cumulative / len(ticker_symbols)

    return results, total_return_cumulative, average_return, max_drawdown_cumulative, average_volatility

# Plages de paramètres pour l'optimisation
stop_loss_range = [0.1]
take_profit_range = [0.2]

# Stockage des résultats d'optimisation
optimization_results = []

# Liste des symboles boursiers à tester
ticker_symbols = get_sp500_symbols()

for stop_loss in stop_loss_range:
    for take_profit in take_profit_range:
        backtest_result, total_return, average_return, max_drawdown, average_volatility = backtest_multiple_stocks(ticker_symbols, "2020-01-01", "2023-12-06", stop_loss, take_profit)
        
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
