import pandas as pd
import requests
from datetime import datetime, timedelta
from constants import CRYPTO_COMPARE_API
from func_connect import fetch_minute_data

api_key = CRYPTO_COMPARE_API
symbol = 'BTC'
to_symbol = 'USDT'
start_time = datetime.now() - timedelta(days=365)
end_time = datetime.now()

# Define chunk size
chunk_size = 300  # minutes

# Define output directory
output_dir = './minute_data/'

# Loop through each chunk of time
while end_time > start_time:
    # Calculate chunk start and end times
    chunk_end_time = end_time
    chunk_start_time = chunk_end_time - timedelta(minutes=chunk_size)
    
    # Fetch minute data for the chunk
    chunk_data = fetch_minute_data(symbol, api_key, chunk_start_time, chunk_end_time, to_symbol)
    
    # Save the chunk data to a CSV file
    filename = f"{symbol}_minute_data_{chunk_start_time.strftime('%Y-%m-%d_%H-%M')}_to_{chunk_end_time.strftime('%Y-%m-%d_%H-%M')}.csv"
    filepath = output_dir + filename
    chunk_data.to_csv(filepath)
    
    # Move the chunk end time back by chunk size
    end_time = chunk_start_time