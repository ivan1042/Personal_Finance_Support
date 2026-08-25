# Portfolio Dashboard

An interactive Streamlit dashboard for analyzing a portfolio of stock tickers. Enter tickers, allocation weights, and an investment horizon to view historical data, portfolio metrics, and simulated outcomes.

> **Educational use only.** Outputs are exploratory calculations, not investment advice or a prediction of future returns.

## What it shows

- Portfolio allocation pie chart
- Expected monthly return, volatility, Sharpe ratio, Sortino ratio, Value at Risk, and maximum drawdown
- Historical weighted portfolio returns
- Company information returned by Yahoo Finance
- 100-path Monte Carlo simulation using historical return covariance
- A retirement-amount calculation available in the analytics layer

## Run it

From the repository root, after installing [the project dependencies](../README.md#quick-start):

```powershell
streamlit run Portfolio_dashboard/webpage.py
```

In VS Code, press `F5` and choose **Run Personal Finance dashboard**.

## How to use it

1. Enter comma-separated ticker symbols, such as `AAPL, GOOG`.
2. Enter the matching weights, such as `0.7, 0.3`.
3. Ensure the weights add up to `1`.
4. Choose an investment horizon from 1 to 40 years.
5. Select **Analyze Portfolio**.

On first use, historical monthly price data is downloaded through `yfinance` and cached in `../data/`.

## Main components

| File or folder | Responsibility |
| --- | --- |
| `webpage.py` | Streamlit user interface and charts |
| `analysis.py` | Coordinates data retrieval, metrics, and simulations |
| `analytics/returns.py` | Arithmetic/geometric return calculations and portfolio history |
| `analytics/risk.py` | VaR, volatility, Sharpe, Sortino, and drawdown calculations |
| `analytics/monte_carlo.py` | Correlated portfolio-path simulation |
| `analytics/retirement.py` | Retirement amount calculation |
| `../service/` | Market-data download, caching, and dataframe preparation |

## Notes and limitations

- The dashboard uses historical monthly returns and a 95% VaR confidence level.
- Simulations use an initial amount of $10,000 and run 100 paths in the current implementation.
- Market data is provided by Yahoo Finance and may be delayed, incomplete, or revised.

