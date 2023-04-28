import requests
import pandas as pd

def fetch_hourly_data(symbol, to_symbol='USDT', limit=2000, aggregate=1):
    url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={symbol}&tsym={to_symbol}&limit={limit}&aggregate={aggregate}"
    response = requests.get(url)
    data = response.json()

    if data['Response'] == 'Success':
        rows = data['Data']['Data']
        df = pd.DataFrame(rows)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
        return df
    else:
        print(f"Error fetching data for {symbol}: {data['Message']}")
        return None

symbol = 'BTC'
hourly_data = fetch_hourly_data(symbol)
print(hourly_data.head())