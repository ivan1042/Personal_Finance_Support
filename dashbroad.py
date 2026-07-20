from service import yahoo
from service import dataframe
from service import info
from analytics import risk
from analytics import returns
from analytics import retirement
from analytics import monte_carlo
import pandas as pd

def analysis(stocks = ["VFINX", "AAPL"], weight = [0.7, 0.3], timeframe = 40):
    raw_data = []
    data = []
    raw_mon_return_temp = []
    art_return_temp = []
    ticker_info = []

    for stock in stocks:
        yahoo.get_historical_data(stock)
        ticker_info.append(info.ticker_info(stock))
        raw_data.append(dataframe.stats(stock))

    for k in raw_data:
        data.append(returns.returns(k))

    for k in range(0, len(stocks)):
        raw_mon_return_temp.append(raw_data[k]["%Change"])
        art_return_temp.append(data[k][0])
        risk.risk_calc(raw_data[k], *data[k])

    for k in data:
        retirement.retirement_amount(k[2])

    sim_result = monte_carlo.simulation(raw_mon_return_temp, art_return_temp, stocks, weight, timeframe)

    return ticker_info, sim_result


"""historical_VaR = risk.historical_VaR
print(returns.monthly_geo_mean)
print(risk.sharpe_ratio)
print(risk.sortino_ratio)
print(risk.max_drawdown)"""