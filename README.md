# Parametric Portfolio VaR Calculator

## Project Overview

This project provides an Object-Oriented implementation of a Parametric Value at Risk (VaR) calculator for a financial portfolio. The program downloads historical price data, calculates log returns, and estimates portfolio VaR at different confidence levels. Additionally, it visualizes the distribution of portfolio returns and highlights VaR thresholds for easy interpretation.

## Features

- **Log Returns Calculation**: Computes log returns for a portfolio based on historical price data.
- **Covariance Matrix**: Calculates the annualized covariance matrix for the portfolio's assets.
- **Portfolio VaR Estimation**: Provides parametric VaR at different confidence levels (90%, 95%, and 99%) over a user-specified number of days.
- **Histogram Plotting**: Visualizes the distribution of portfolio returns and overlays VaR thresholds.
- **Object-Oriented Design**: Encapsulates functionality in a `Portfolio` class for easy extensibility and reuse.

## Dependencies

- Python 3.8+
- `numpy`
- `pandas`
- `matplotlib`
- `scipy`
- `yfinance`

You can install these dependencies with the following command:
```bash
pip install numpy pandas matplotlib scipy yfinance
