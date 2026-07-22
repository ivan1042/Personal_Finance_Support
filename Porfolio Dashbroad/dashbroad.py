from pathlib import Path
import sys
service_root = Path(__file__).resolve().parent.parent
sys.path.append(str(service_root))
from service import yahoo
from service import dataframe
from service import info
from analytics import risk
from analytics import returns
from analytics import retirement
from analytics import monte_carlo


class analysis(stocks = ["VFINX", "AAPL"], weight = [0.7, 0.3], timeframe = 40):
    def __init__(self, stocks, weight, timeframe):
        self.stocks = stocks
        self.weight = weight
        self.timeframe = timeframe

        self.raw_data = []
        self.data = []
        self.raw_mon_return_temp = []
        self.art_return_temp = []
        self.ticker_info = []


        for stock in self.stocks:
            yahoo.get_historical_data(stock)
            self.ticker_info.append(info.ticker_info(stock))
            self.raw_data.append(dataframe.stats(stock))

        for k in self.raw_data:
            self.data.append(returns.returns(k))

        for k in range(0, len(stocks)):
            self.raw_mon_return_temp.append(self.raw_data[k]["%Change"])
            self.art_return_temp.append(self.data[k][0])
            risk.risk_calc(self.raw_data[k], *self.data[k])

        for k in self.data:
            retirement.retirement_amount(k[2])

        sim_result = monte_carlo.simulation(self.raw_mon_return_temp, self.art_return_temp, stocks, weight, timeframe)




"""historical_VaR = risk.historical_VaR
print(returns.monthly_geo_mean)
print(risk.sharpe_ratio)
print(risk.sortino_ratio)
print(risk.max_drawdown)"""