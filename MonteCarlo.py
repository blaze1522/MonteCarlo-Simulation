import pandas_datareader.data as web
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

# The basic parameters of the stock (yyyy, mm, dd), 'listing on the yfinance'
start = dt.datetime(2019, 4, 16)
end = dt.datetime(2020, 4, 16)
stock = 'AAPL'

# We will request yahoo finance api to send us the data
prices = web.DataReader(stock, 'yahoo', start, end)['Close']
returns = prices.pct_change()

# All random walks are conditioned to the last known price
last_price = prices[-1]

num_simulations = 100
num_days = 252

simulation_df = pd.DataFrame()

# SImulating
for x in range(num_simulations):
    count = 0
    # Simple gives the std.dev. of daily returns as a measure of volitility
    daily_vol = returns.std()

    price_series = []

    price = last_price * (1 + np.random.normal(0, daily_vol))
    price_series.append(price)

    for y in range(num_days):
        if count == 251:
            break
        price = price_series[count] * (1 + np.random.normal(0, daily_vol))
        price_series.append(price)
        count += 1

    simulation_df[x] = price_series

# Plotting
fig = plt.figure()
plt.plot(simulation_df)
plt.axhline(y=last_price, color='r', linestyle='-')
plt.xlabel('Day')
plt.ylabel('Price')
plt.title('Monte Carlo Simulation: {0:7s}'.format(stock))
plt.show()
