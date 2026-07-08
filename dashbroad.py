import pandas as pd
import numpy as np
from analytics import risk
from analytics import returns
from analytics import retirement
from analytics import monte_carlo

stocks = ["VFINX", "AAPL"]
weight = [0.7, 0.3]
data = []
raw_mon_return_temp = []
geo_return_temp = []
for stock in stocks:
    data.append(returns.stats(stock))

for k in range(0, len(stocks)):
    raw_mon_return_temp.append(data[k][0]["%Change"])
    geo_return_temp.append(data[k][3])


for k in data:
    print(risk.risk_calc(*k))
for k in data:
    print(retirement.retirement_amount(k[3]))

monte_carlo.simulation(raw_mon_return_temp, geo_return_temp, stocks, weight )

"""historical_VaR = risk.historical_VaR
print(returns.monthly_geo_mean)
print(risk.sharpe_ratio)
print(risk.sortino_ratio)
print(risk.max_drawdown)"""