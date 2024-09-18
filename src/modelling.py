
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from scipy.stats import norm

class Portfolio:
    def __init__(self, tickers, portfolio_value=1000000, years=15, weights=None):
        
        self.tickers = tickers
        self.portfolio_value = portfolio_value
        self.end_date = dt.datetime.now()
        self.start_date = self.end_date - dt.timedelta(days=365 * years)
        self.weights = np.array(weights) if weights else np.array([1 / len(tickers)] * len(tickers))
        self.adj_close_df = self._download_data()
        self.log_returns = self._calculate_log_returns()

    def _download_data(self):
        """Download adjusted close prices for the tickers."""
        return yf.download(self.tickers, start=self.start_date, end=self.end_date)['Adj Close']

    def _calculate_log_returns(self):
        """Calculate the log returns for the portfolio."""
        return np.log(self.adj_close_df / self.adj_close_df.shift(1)).dropna()

    def calculate_historical_returns(self, days=5):
        """Calculate the rolling sum of log returns over a specified window."""
        historical_returns = (self.log_returns * self.weights).sum(axis=1)
        return historical_returns.rolling(window=days).sum()

    def calculate_cov_matrix(self):
        """Calculate the annualized covariance matrix of returns."""
        return self.log_returns.cov() * 252

    def calculate_portfolio_std(self):
        """Calculate the portfolio standard deviation."""
        cov_matrix = self.calculate_cov_matrix()
        return np.sqrt(self.weights.T @ cov_matrix @ self.weights)

    def calculate_parametric_var(self, days=5, confidence_levels=[0.9, 0.95, 0.99]):
        """Calculate VaR based on parametric estimation for different confidence levels."""
        portfolio_std_dev = self.calculate_portfolio_std()
        VaRs = {}
        for cl in confidence_levels:
            VaR = self.portfolio_value * portfolio_std_dev * norm.ppf(cl) * np.sqrt(days / 252)
            VaRs[cl] = VaR
        return VaRs

    def plot_var_distribution(self, days=5, confidence_levels=[0.9, 0.95, 0.99]):
        """Plot the histogram of portfolio returns and the VaR thresholds."""
        historical_returns = self.calculate_historical_returns(days=days)
        historical_x_day_returns_dollar = historical_returns * self.portfolio_value

        VaRs = self.calculate_parametric_var(days=days, confidence_levels=confidence_levels)

        plt.hist(historical_x_day_returns_dollar, bins=50, density=True, alpha=0.5, label=f'{days}-Day Returns')
        for cl, VaR in VaRs.items():
            plt.axvline(x=-VaR, linestyle='--', color='red', label=f'VaR at {int(cl*100)}% Confidence')
        plt.xlabel(f'{days}-Day Portfolio Return ($)')
        plt.ylabel('Frequency')
        plt.title(f'Distribution of Portfolio {days}-Day Returns and Parametric VaR Estimates')
        plt.legend()
        plt.show()

    def run_var_analysis(self, days=5, confidence_levels=[0.9, 0.95, 0.99]):
        """Run the complete VaR analysis and print the results."""
        VaRs = self.calculate_parametric_var(days=days, confidence_levels=confidence_levels)
        for cl, VaR in VaRs.items():
            print(f"{cl*100:>6.0f}%': {'':<8} ${VaR:>10,.2f}")
        self.plot_var_distribution(days=days, confidence_levels=confidence_levels)


