# Personal Finance Support

Python tools for exploring market data, portfolio risk, and personal-finance scenarios. The repository contains two active subprojects that share a small Yahoo Finance data service.

> **Educational use only.** This project is for research and learning, not investment advice. Historical results and simulations do not guarantee future performance.

## Projects

| Project | Purpose | Entry point |
| --- | --- | --- |
| [Portfolio Dashboard](Portfolio_dashboard/README.md) | Analyze a user-defined portfolio, view risk/return metrics, simulate possible paths, and explore retirement estimates. | `Portfolio_dashboard/webpage.py` |
| [Stock Analysis](<Stock analysis/README.md>) | Explore individual-stock volatility and beta indicators, visualizations, and experimental trading signals. | `Stock analysis/visualization.py` |

## Features

- Downloads and caches historical market data with [yfinance](https://github.com/ranaroussi/yfinance)
- Interactive Streamlit and Plotly dashboards
- Portfolio allocation, historical return, and Monte Carlo visualizations
- Return, volatility, Value at Risk (VaR), Sharpe ratio, Sortino ratio, and drawdown calculations
- Stock-level volatility and beta indicator exploration

## Quick start

### 1. Clone and open the project

```powershell
git clone https://github.com/ivan1042/Personal_Finance_Support.git
cd Personal_Finance_Support
```

### 2. Create a virtual environment and install dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 3. Run a tool

Portfolio Dashboard:

```powershell
streamlit run Portfolio_dashboard/webpage.py
```

Stock Analysis:

```powershell
streamlit run "Stock analysis/visualization.py"
```

Streamlit will print a local URL, usually `http://localhost:8501`, to open in your browser.

## Repository layout

```text
.
+-- Portfolio_dashboard/   # Portfolio and retirement dashboard
+-- Stock analysis/        # Stock indicator exploration and signal experiments
+-- service/               # Yahoo Finance download, cache, and dataframe helpers
+-- data/                  # Downloaded market-data cache (not committed)
+-- requirements.txt       # Python dependencies
`-- .vscode/               # Shared VS Code run configuration
```

## Development notes

- The first analysis of a ticker downloads historical data and saves it under `data/`. Later runs reuse the cached CSV file.
- Tickers and data availability are supplied by Yahoo Finance through `yfinance` and can change without notice.
- The VS Code debugger includes **Run Personal Finance dashboard**; press `F5` after opening the repository.

## Next steps

The project is actively evolving. Useful next improvements include automated tests, pinned dependency versions, input validation, documented methodology, and backtest performance reporting.
