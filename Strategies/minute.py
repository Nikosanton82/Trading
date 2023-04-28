from datetime import datetime, timedelta
from constants import CRYPTO_COMPARE_API
from func_connect import fetch_minute_data
import pandas as pd


api_key = CRYPTO_COMPARE_API  # Replace with your actual API key
symbols = ['BTC', 'ETH', 'LTC', 'XRP', 'BCH', 'ADA', 'DOT', 'LINK', 'BNB', 'XLM']  # List of symbols

# Calculate the start and end times for the past 7 days
end_time = datetime.now() - timedelta(minutes=1)
start_time = end_time - timedelta(days=7)

for symbol in symbols:
    # Initialize an empty DataFrame to store the data
    minute_data = pd.DataFrame()

    # Set the initial chunk end time to the final end_time
    chunk_end_time = end_time

    # Loop until the start_time is reached
    while chunk_end_time > start_time:
        # Calculate the chunk start time by subtracting 1 day from the chunk end time
        chunk_start_time = chunk_end_time - timedelta(days=1)
        
        # Make sure the chunk start time doesn't go beyond the overall start_time
        if chunk_start_time < start_time:
            chunk_start_time = start_time

        # Fetch the minute data for the current chunk
        chunk_data = fetch_minute_data(symbol, api_key, chunk_start_time, chunk_end_time)

        if chunk_data is not None:
            # Concatenate the fetched chunk data with the existing data
            minute_data = pd.concat([chunk_data, minute_data])

        # Set the next chunk end time to the current chunk start time
        chunk_end_time = chunk_start_time

    # Save the fetched minute data to a new DataFrame
    minute_data_final = minute_data.copy()

    # Export the data to a CSV file
    minute_data_final.to_csv(f'{symbol}_minute_data_past_7_days.csv')

    print(f"{symbol} minute data:")
    print(minute_data_final)
    print("\n")