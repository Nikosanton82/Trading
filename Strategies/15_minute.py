from datetime import datetime, timedelta
from constants import CRYPTO_COMPARE_API
from func_connect import fetch_minute_data
import pandas as pd
import os 

api_key = CRYPTO_COMPARE_API
symbols = ['BTC', 'ETH', 'LTC', 'XRP', 'BCH', 'ADA', 'DOT', 'LINK', 'BNB', 'XLM']
end_time = datetime.now() - timedelta(minutes=15)
start_time = end_time - timedelta(days=30)

aggregate = 15  # 15-minute intervals

for symbol in symbols:
    df_symbol = pd.DataFrame()

    while end_time > start_time:
        chunk_start_time = end_time - timedelta(days=1)
        if chunk_start_time < start_time:
            chunk_start_time = start_time

        chunk_data = fetch_minute_data(symbol, api_key, chunk_start_time, end_time, aggregate)
        if chunk_data is not None:
            df_symbol = pd.concat([chunk_data, df_symbol])

        end_time = chunk_start_time - timedelta(minutes=15)

    df_symbol.to_csv(f"{symbol}_15min_data_past_30_days.csv")

closing_values = {}

for symbol in symbols:
    file_path = f"{symbol}_15min_data_past_30_days.csv"
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, index_col='time', parse_dates=True)
        closing_values[symbol] = df['close']

closing_values_df = pd.DataFrame(closing_values)
closing_values_df.to_csv("closing_values_15min_past_30_days.csv")