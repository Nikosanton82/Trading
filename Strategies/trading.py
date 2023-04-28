import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
from itertools import combinations

# List of 50 most traded stocks (tickers)
stocks = [
    "AAPL", "MSFT", "AMZN", "META", "GOOGL", "GOOG", "TSLA", "NVDA", "BRK-B", "JPM",
    "JNJ", "UNH", "V", "PG", "HD", "MA", "DIS", "BAC", "ADBE", "CRM", "CMCSA",
    "VZ", "NFLX", "XOM", "KO", "INTC", "CSCO", "PEP", "PFE", "T", "MRK", "WMT",
    "ABT", "TMO", "AMGN", "MMM", "MCD", "NKE", "LLY", "UNP", "MDT", "AVGO",
    "IBM", "TXN", "QCOM", "GILD", "FIS", "HON", "ACN"
]

# Download historical data for the stocks
start_date = "2000-01-01"
end_date = "2023-04-27"

stock_data = {}
for stock in stocks:
    stock_data[stock] = yf.download(stock, start=start_date, end=end_date)

# Calculate daily returns for each stock
for stock, data in stock_data.items():
    data['returns'] = data['Adj Close'].pct_change().dropna()

# Calculate correlations between stock returns
corr_matrix = pd.DataFrame(index=stocks, columns=stocks)
for i, stock1 in enumerate(stocks):
    for j, stock2 in enumerate(stocks):
        corr_matrix.iloc[i, j] = stock_data[stock1]['returns'].corr(stock_data[stock2]['returns'])

print("Correlation matrix of stock returns:")
print(corr_matrix)

# Test for cointegration between each pair of stocks
coint_matrix = pd.DataFrame(index=stocks, columns=stocks)
cointegrated_pairs = []

for stock1, stock2 in combinations(stocks, 2):
    _, p_value, _ = coint(stock_data[stock1]['Adj Close'], stock_data[stock2]['Adj Close'])
    coint_matrix.loc[stock1, stock2] = p_value
    coint_matrix.loc[stock2, stock1] = p_value

    # Check for cointegration with a 5% significance level
    if p_value < 0.05:
        cointegrated_pairs.append((stock1, stock2))

print("Cointegration matrix:")
print(coint_matrix)

# Backtest pairs trading strategy for cointegrated pairs
entry_threshold = 2
exit_threshold = 0.5

def kelly_criterion(win_rate, win_loss_ratio):
    return win_rate - (1 - win_rate) / win_loss_ratio

for stock1, stock2 in cointegrated_pairs:
    # Estimate the hedge ratio using linear regression
    x = sm.add_constant(stock_data[stock1]['Adj Close'])
    y = stock_data[stock2]['Adj Close']
    model = sm.OLS(y, x).fit()
    hedge_ratio = model.params[stock1]

    # Calculate the spread
    spread = stock_data[stock2]['Adj Close'] - hedge_ratio * stock_data[stock1]['Adj Close']
    spread_mean = spread.mean()
    spread_std = spread.std()

    # Backtest the strategy
    position = 0
    pnl = []
    for date, value in spread.items():
        if position == 0:
            if value > spread_mean + entry_threshold * spread_std:
                position = -1  # Enter short position
            elif value < spread_mean - entry_threshold * spread_std:
                position = 1  # Enter long position
        else:
            if position == 1 and value > spread_mean - exit_threshold * spread_std:
                position = 0  # Exit long position
            elif position == -1 and value < spread_mean + exit_threshold * spread_std:
                position = 0  # Exit short position

        # Calculate PnL
        if position == 1:
            daily_pnl = -stock_data[stock1]['returns'][date] + hedge_ratio * stock_data[stock2]['returns'][date]
        elif position == -1:
            daily_pnl = stock_data[stock1]['returns'][date] - hedge_ratio * stock_data[stock2]['returns'][date]
        else:
            daily_pnl = 0

        pnl.append(daily_pnl)

    # Calculate the cumulative PnL of the strategy
    cum_pnl = np.cumsum(pnl)
    plt.figure(figsize=(15, 5))
    plt.plot(spread.index, cum_pnl)
    plt.title(f"{stock1} and {stock2} Pairs Trading Strategy Cumulative PnL")
    plt.ylabel("Cumulative PnL")
    plt.xlabel("Date")
    plt.show()

    # Calculate win rate and win/loss ratio
    winning_trades = [trade for trade in pnl if trade > 0]
    losing_trades = [trade for trade in pnl if trade < 0]
    win_rate = len(winning_trades) / len(pnl)
    win_loss_ratio = abs(np.mean(winning_trades) / np.mean(losing_trades))

    # Calculate the Kelly criterion
    kelly_fraction = kelly_criterion(win_rate, win_loss_ratio)

    # Adjust position sizes based on the Kelly criterion
    adjusted_pnl = [trade * kelly_fraction for trade in pnl]

    # Calculate the cumulative PnL of the strategy after applying the Kelly criterion
    cum_pnl = np.cumsum(adjusted_pnl)
    plt.figure(figsize=(15, 5))
    plt.plot(spread.index, cum_pnl)
    plt.title(f"{stock1} and {stock2} Pairs Trading Strategy Cumulative PnL (Kelly Criterion)")
    plt.ylabel("Cumulative PnL")
    plt.xlabel("Date")
    plt.show()

