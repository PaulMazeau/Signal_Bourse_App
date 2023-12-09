import pandas as pd

def get_sp500_symbols():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tables = pd.read_html(url)
    sp500_table = tables[0]
    symbols = sp500_table['Symbol']
    return symbols.tolist()

def save_to_json(symbols, filename="sp500_symbols.json"):
    import json
    with open(filename, 'w') as file:
        json.dump(symbols, file)

if __name__ == "__main__":
    symbols = get_sp500_symbols()
    save_to_json(symbols)
    print(f"Les symboles du S&P 500 ont été sauvegardés dans le fichier 'sp500_symbols.json'.")
