import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from statsmodels.tsa.seasonal import seasonal_decompose

class FinancialAnalyzer:
    def __init__(self):
        """Initialize the FinancialAnalyzer with an empty data dictionary."""
        self.data = {}

    def fetch_data(self, symbols, start_date, end_date):
        """
        Fetch historical stock data for the given symbols within the specified date range.
        Uses Yahoo Finance as the data source.
        """
        for symbol in symbols:
            try:
                logging.info(f"Fetching data for {symbol} from {start_date} to {end_date}")
                df = yf.download(symbol, start=start_date, end=end_date)
                df.reset_index(inplace=True)
                self.data[symbol] = df
                logging.info(f"Data fetched successfully for {symbol}")
            except Exception as e:
                logging.error(f"Error fetching data for {symbol}: {e}")
        return self.data

    def clean_data(self):
        """
        Clean the data by handling missing values using forward fill and removing rows
        with remaining missing values.
        """
        for symbol, df in self.data.items():
            try:
                logging.info(f"Cleaning data for {symbol}")
                df['Date'] = pd.to_datetime(df['Date'])
                df.fillna(method='ffill', inplace=True)
                df.dropna(inplace=True)
                logging.info(f"Data cleaned successfully for {symbol}")
            except Exception as e:
                logging.error(f"Error cleaning data for {symbol}: {e}")
        return self.data

    def calculate_volatility(self):
        """
        Calculate the volatility (standard deviation) of the daily returns for each symbol.
        """
        volatility = {}
        for symbol, df in self.data.items():
            try:
                logging.info(f"Calculating volatility for {symbol}")
                df['Daily Return'] = df['Close'].pct_change()
                volatility[symbol] = df['Daily Return'].std()
            except Exception as e:
                logging.error(f"Error calculating volatility for {symbol}: {e}")
        return volatility

    def plot_price_histogram(self):
        """
        Plot the histogram of closing prices for each symbol to visualize the price distribution.
        """
        for symbol, df in self.data.items():
            try:
                logging.info(f"Plotting price histogram for {symbol}")
                plt.figure(figsize=(10, 6))
                plt.hist(df['Close'], bins=30, color='blue', alpha=0.7, label=f'{symbol} Closing Price')
                plt.title(f'{symbol} Closing Price Distribution')
                plt.xlabel('Price')
                plt.ylabel('Frequency')
                plt.legend()
                plt.show()
            except Exception as e:
                logging.error(f"Error plotting price histogram for {symbol}: {e}")

    def plot_cumulative_returns(self):
        """
        Plot the cumulative returns over time for each symbol.
        """
        for symbol, df in self.data.items():
            try:
                logging.info(f"Plotting cumulative returns for {symbol}")
                df['Daily Return'] = df['Close'].pct_change()
                df['Cumulative Return'] = (1 + df['Daily Return']).cumprod() - 1
                plt.figure(figsize=(14, 6))
                plt.plot(df['Date'], df['Cumulative Return'], label=f'{symbol} Cumulative Return')
                plt.title(f'{symbol} Cumulative Return Over Time')
                plt.xlabel('Date')
                plt.ylabel('Cumulative Return')
                plt.legend()
                plt.show()
            except Exception as e:
                logging.error(f"Error plotting cumulative returns for {symbol}: {e}")

    def calculate_moving_average(self, window=50):
        """
        Calculate and add a moving average to the data for each symbol.
        """
        for symbol, df in self.data.items():
            try:
                logging.info(f"Calculating moving average for {symbol} with window {window}")
                df[f'{window}-Day MA'] = df['Close'].rolling(window=window).mean()
            except Exception as e:
                logging.error(f"Error calculating moving average for {symbol}: {e}")
        return self.data

    def plot_moving_average(self):
        """
        Plot the closing price along with its moving average for each symbol.
        """
        for symbol, df in self.data.items():
            try:
                logging.info(f"Plotting moving average for {symbol}")
                plt.figure(figsize=(14, 6))
                plt.plot(df['Date'], df['Close'], label=f'{symbol} Close Price')
                plt.plot(df['Date'], df[f'50-Day MA'], label='50-Day Moving Average', color='orange')
                plt.title(f'{symbol} Closing Price and Moving Average')
                plt.xlabel('Date')
                plt.ylabel('Price')
                plt.legend()
                plt.show()
            except Exception as e:
                logging.error(f"Error plotting moving average for {symbol}: {e}")

    def calculate_sharpe_ratio(self):
        """
        Calculate the Sharpe ratio for each symbol.
        """
        sharpe_ratios = {}
        for symbol, df in self.data.items():
            try:
                logging.info(f"Calculating Sharpe ratio for {symbol}")
                df['Daily Return'] = df['Close'].pct_change()
                sharpe_ratio = df['Daily Return'].mean() / df['Daily Return'].std() * np.sqrt(252)
                sharpe_ratios[symbol] = sharpe_ratio
            except Exception as e:
                logging.error(f"Error calculating Sharpe ratio for {symbol}: {e}")
        return sharpe_ratios

    def decompose_trends(self):
        """
        Decompose the time series into trend, seasonal, and residual components.
        """
        decompositions = {}
        for symbol, df in self.data.items():
            try:
                logging.info(f"Decomposing time series for {symbol}")
                df.set_index('Date', inplace=True)
                decomposition = seasonal_decompose(df['Close'], model='multiplicative', period=252)
                decomposition.plot()
                plt.suptitle(f'{symbol} Seasonal Decomposition')
                plt.show()
                decompositions[symbol] = decomposition
                df.reset_index(inplace=True)  # Reset index for further use
            except Exception as e:
                logging.error(f"Error decomposing time series for {symbol}: {e}")
        return decompositions

    def calculate_max_drawdown(self):
        """
        Calculate the maximum drawdown for each symbol.
        """
        drawdowns = {}
        for symbol, df in self.data.items():
            try:
                logging.info(f"Calculating maximum drawdown for {symbol}")
                df['Cumulative Return'] = (1 + df['Close'].pct_change()).cumprod() - 1
                df['Peak'] = df['Cumulative Return'].cummax()
                df['Drawdown'] = df['Cumulative Return'] - df['Peak']
                max_drawdown = df['Drawdown'].min()
                drawdowns[symbol] = max_drawdown
            except Exception as e:
                logging.error(f"Error calculating max drawdown for {symbol}: {e}")
        return drawdowns
