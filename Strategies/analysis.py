from func_connect import fetch_top_n_coins, fetch_hourly_data
from constants import CRYPTO_COMPARE_API
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


api_key = CRYPTO_COMPARE_API  # Replace with your actual API key
top_10_coins = fetch_top_n_coins(api_key)

# Function to compute moving averages
def moving_average(data, window):
    return data.rolling(window=window).mean()

# Function to compute moving averages
def moving_average(data, window):
    return data.rolling(window=window).mean()

# Function to calculate percentage change
def percentage_change(data):
    return data.pct_change()

# Function to plot the price and moving averages
def plot_price_and_moving_averages(symbol, hourly_data):
    plt.figure(figsize=(15, 6))
    plt.plot(hourly_data.index, hourly_data['close'], label='Price')
    plt.plot(hourly_data.index, moving_average(hourly_data['close'], 7 * 24), label='7-day MA')
    plt.plot(hourly_data.index, moving_average(hourly_data['close'], 30 * 24), label='30-day MA')
    plt.title(f"{symbol} Hourly Price and Moving Averages")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.show()

if top_10_coins is not None:
    limit = 30 * 24

    hourly_data_list = []
    for coin in top_10_coins:
        hourly_data = fetch_hourly_data(coin, api_key, limit=limit)
        print(f"{coin} hourly data:")
        print(hourly_data.head())
        print("\n")
        
        hourly_data_list.append(hourly_data['close'])
        
        # Plot the price and moving averages for each cryptocurrency
        plot_price_and_moving_averages(coin, hourly_data)

    # Concatenate hourly data for all cryptocurrencies
    combined_data = pd.concat(hourly_data_list, axis=1, keys=top_10_coins)
    
    # Calculate the hourly percentage change for each cryptocurrency
    pct_changes = percentage_change(combined_data)
    
    # Compute the correlation between different cryptocurrencies
    correlation = pct_changes.corr()
    
    print("Correlation between cryptocurrencies:")
    print(correlation)


