# filename: plot_stock_prices.py
import yfinance as yf
import matplotlib.pyplot as plt

# Define the stock symbols and the date range
stocks = ["META", "TSLA"]
start_date = "2020-01-01"
end_date = "2023-10-01"

# Download the stock data
data = yf.download(stocks, start=start_date, end=end_date)['Close']

# Plotting the stock prices
plt.figure(figsize=(14, 7))
for stock in stocks:
    plt.plot(data.index, data[stock], label=stock)

plt.title('META and TESLA Stock Price Change')
plt.xlabel('Date')
plt.ylabel('Stock Price (USD)')
plt.legend()
plt.grid()
plt.show()