
from src.modelling import Portfolio

if __name__ == "__main__":
    
    portfolio = Portfolio(tickers=['SPY', 'BND', 'GLD', 'QQQ', 'VTI'],
                          portfolio_value=1000,
                          years=15)
    
    portfolio.run_var_analysis(days=22)