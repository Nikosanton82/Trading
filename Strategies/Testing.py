import pandas as pd
import matplotlib.pyplot as plt

symbols = ['BTC', 'ETH', 'LTC', 'XRP', 'BCH', 'ADA', 'DOT', 'LINK', 'BNB', 'XLM']  # List of symbols

# Initialize an empty DataFrame to store the closing values
closing_values = pd.DataFrame()

# Loop through each symbol
for symbol in symbols:
    # Read the CSV file for the symbol
    csv_file = f"{symbol}_minute_data_past_7_days.csv"
    data = pd.read_csv(csv_file, index_col=0, parse_dates=True)
    
    # Extract the closing values
    close_data = data[['close']]
    close_data.columns = [symbol]
    
    # Merge the closing values into the main DataFrame
    if closing_values.empty:
        closing_values = close_data
    else:
        closing_values = closing_values.join(close_data, how='outer')

# Save the closing values to a new DataFrame
closing_values_final = closing_values.copy()

# Drop the missing values
closing_values_final = closing_values.dropna()

# Calculate the returns
returns_final = closing_values_final.pct_change()

# Plot the closing values
fig, axes = plt.subplots(nrows=len(symbols), ncols=1, figsize=(10, 30), sharex=True)
fig.suptitle('Closing Prices')

for i, symbol in enumerate(symbols):
    axes[i].plot(closing_values_final[symbol], label=symbol)
    axes[i].set_title(symbol)
    axes[i].legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.97])
plt.show()

# Plot the returns
fig, axes = plt.subplots(nrows=len(symbols), ncols=1, figsize=(10, 30), sharex=True)
fig.suptitle('Returns')

for i, symbol in enumerate(symbols):
    axes[i].plot(returns_final[symbol], label=symbol)
    axes[i].set_title(symbol)
    axes[i].legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.97])
plt.show()