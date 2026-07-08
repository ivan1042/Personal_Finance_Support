from analytics import risk
from analytics import returns
from analytics import retirement

stock = ["VFINX", "AAPL"]
data = []

for stock in stock:
    data.append(returns.stats(stock))


for k in data:
    print(risk.risk_calc(*k))

for k in data:
    print(retirement.retirement_amount(k[3]))

"""historical_VaR = risk.historical_VaR
print(returns.monthly_geo_mean)
print(risk.sharpe_ratio)
print(risk.sortino_ratio)
print(risk.max_drawdown)"""