import yfinance as yf
import os

# Define the assets and date range
symbols = ['GC=F', 'CL=F', '^GSPC', '^GDAXI', 'EURUSD=X', 'GBPUSD=X', 'CSIQ', 'BTC-USD', 'ETH-USD', 'OPENAI']
start_date = '2003-01-01'
end_date = '2023-04-28'

# Create a directory to store the downloaded data
if not os.path.exists('daily'):
    os.makedirs('daily')

# Download the historical data using yfinance for each asset
for symbol in symbols:
    data = yf.download(symbol, start=start_date, end=end_date, interval='1d')
    # Save the data to a CSV file
    data.to_csv(f'daily/{symbol}_daily.csv', index=True)
    print(f"Downloaded {symbol} data")
