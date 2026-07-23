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


class analysis():
    def __init__(self, stocks = ["VFINX", "AAPL"], weight = [0.7, 0.3], timeframe = 40):
        self.stocks = stocks
        self.weight = weight
        self.timeframe = timeframe

        self.raw_data = []
        self.data = []
        self.risk_data = []
        self.raw_mon_return_temp = []
        self.raw_mon_close = []
        self.monthly_art_mean = []
        self.monthly_geo_mean = []
        self.ticker_info = []
        self.historical_VaR = []
        self.parametric_VaR = []
        self.sharpe_ratio = []
        self.sortino_ratio = []
        self.max_drawdown = []
        self.volatility = []

        for stock in self.stocks:
            #yahoo.get_historical_data(stock)
            self.ticker_info.append(info.ticker_info(stock))
            self.raw_data.append(dataframe.stats(stock))

        for k in self.raw_data:
            self.data.append(returns.returns(k))

        for k in range(0, len(stocks)):
            self.risk_data.append(risk.risk_calc(self.raw_data[k], *self.data[k]))

        for k in range(0, len(stocks)):
            self.raw_mon_close.append(self.raw_data[k]["Close"])
            self.raw_mon_return_temp.append(self.raw_data[k]["%Change"])
            self.monthly_art_mean.append(self.data[k][0])
            self.monthly_geo_mean.append(self.data[k][2])
            self.historical_VaR.append(self.risk_data[k][0])
            self.parametric_VaR.append(self.risk_data[k][1])
            self.sharpe_ratio.append(self.risk_data[k][2])
            self.sortino_ratio.append(self.risk_data[k][3])
            self.max_drawdown.append(self.risk_data[k][4])
            self.volatility.append(self.risk_data[k][5])


        for k in self.data:
            retirement.retirement_amount(k[2])

        self.sim_result = monte_carlo.simulation(self.raw_mon_return_temp, self.monthly_art_mean, self.stocks, self.weight, self.timeframe)
        self.historical_return = returns.port_hist(self.raw_mon_close, self.weight)

