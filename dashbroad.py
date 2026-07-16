from analytics import risk
from analytics import returns
from analytics import retirement
from analytics import monte_carlo
from service import yahoo

stocks = ["VFINX", "AAPL"]
weight = [0.7, 0.3]
data = []
raw_mon_return_temp = []
geo_return_temp = []
for stock in stocks:
    yahoo.get_historical_data(stock)
    data.append(returns.stats(stock))

for k in range(0, len(stocks)):
    raw_mon_return_temp.append(data[k][0]["%Change"])
    geo_return_temp.append(data[k][3])


for k in data:
    risk.risk_calc(*k)
for k in data:
    retirement.retirement_amount(k[3])

print(raw_mon_return_temp, geo_return_temp, stocks, weight)

monte_carlo.simulation(raw_mon_return_temp, geo_return_temp, stocks, weight )

"""historical_VaR = risk.historical_VaR
print(returns.monthly_geo_mean)
print(risk.sharpe_ratio)
print(risk.sortino_ratio)
print(risk.max_drawdown)"""