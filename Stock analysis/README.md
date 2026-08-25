# Stock Analysis

An exploratory Streamlit workspace for examining price history, return distributions, rolling volatility, and beta-based indicators for individual stocks.

> **Educational use only.** The indicators and signal experiments in this folder are not a trading system or investment advice.

## What it explores

- Historical closing prices and daily percentage changes
- Rolling 36-period volatility
- A beta-style indicator calculated against `VFINX`
- High and low volatility/beta observations using 5th and 95th percentiles
- Histograms of daily returns
- Prototype buy/sell signal cleanup and charting

## Run the visualization

From the repository root, after installing [the project dependencies](../README.md#quick-start):

```powershell
streamlit run "Stock analysis/visualization.py"
```

The default visualization compares `NVDA` with `VFINX`. Edit the `target` and `interval` variables in `visualization.py` to explore another symbol or interval.

## Main components

| File | Responsibility |
| --- | --- |
| `parameter.py` | Loads cached data and calculates volatility, beta, and percentile markers |
| `visualization.py` | Primary Streamlit visualization dashboard |
| `tickers.py` | Multi-ticker visualization experiment |
| `backtest.py` | Prototype signal creation and buy/sell charting |

## Data flow

1. `service/lazy_update.py` checks for a ticker's cached CSV.
2. Missing data is downloaded through `yfinance` into `data/`.
3. `service/dataframe.py` prepares close prices, absolute change, percentage change, and return ratios.
4. `parameter.py` computes indicators used by the Streamlit views.

## Notes and limitations

- The current beta calculation and signals are exploratory and have not been validated as a profitable strategy.
- The code uses `VFINX` as its benchmark reference in the current implementation.
- Cached data is reused automatically; delete a ticker's CSV in `data/` if you intentionally want to retrieve it again.

