import requests
import pandas as pd
from datetime import datetime, timedelta


def fetch_minute_data(symbol, api_key, start_time, end_time, to_symbol='USDT'):
    start_timestamp = int(start_time.timestamp())
    end_timestamp = int(end_time.timestamp())
    
    url = f"https://min-api.cryptocompare.com/data/v2/histominute?fsym={symbol}&tsym={to_symbol}&toTs={end_timestamp}&limit=2000&api_key={api_key}"
    response = requests.get(url)
    data = response.json()

    if data['Response'] == 'Success':
        rows = data['Data']['Data']
        df = pd.DataFrame(rows)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
        
        if df.index[0] <= start_time:
            return df.loc[start_time:end_time]
        else:
            print(f"Error fetching data for {symbol}: Data not available for the specified time range")
            return None
    else:
        print(f"Error fetching data for {symbol}: {data['Message']}")
        return None



def fetch_hourly_data(symbol, api_key, to_symbol='USDT', limit=None, aggregate=1):
    url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={symbol}&tsym={to_symbol}&aggregate={aggregate}&api_key={api_key}"
    
    if limit is not None:
        url += f"&limit={limit}"
    
    response = requests.get(url)
    data = response.json()

    if 'Response' not in data or data['Response'] == 'Success':
        rows = data['Data']['Data']
        df = pd.DataFrame(rows)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
        return df
    else:
        print(f"Error fetching data for {symbol}: {data['Message']}")
        return None

def fetch_top_n_coins(api_key, n=10, currency='USD'):
    url = f"https://min-api.cryptocompare.com/data/top/mktcapfull?limit={n}&tsym={currency}&api_key={api_key}"
    response = requests.get(url)
    data = response.json()

    if 'Response' not in data or data['Response'] == 'Success':
        coins = data['Data']
        return [coin['CoinInfo']['Name'] for coin in coins]
    else:
        print(f"Error fetching top {n} coins: {data['Message']}")
        return None


