from pathlib import Path
import sys
service_root = Path(__file__).resolve().parent.parent
sys.path.append(str(service_root))
from service import dataframe
from service import info
from service import lazy_update
from Portfolio_dashboard.risk import static_risk, rolling_risk
from analytics import returns
from analytics import retirement
from analytics import monte_carlo
from Portfolio_dashboard.strategy import Buy_and_hold, Constant_weight


class analysis():
    def __init__(self, stocks, weight, timeframe):
        self.stocks = stocks
        self.weight = weight
        self.timeframe = timeframe

        lazy_update.csv_checker("SHV", "1mo")
        self.risk_free = dataframe.stats("SHV")

        lazy_update.csv_checker("VFINX", "1mo")
        self.benchmark = dataframe.stats("VFINX")

        self.raw_data = []
        self.return_data = []
        self.buy_and_hold = []
        #pending
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
            lazy_update.csv_checker(stock, "1mo")
            self.ticker_info.append(info.ticker_info(stock))
            self.raw_data.append(dataframe.stats(stock))

        self.buy_and_hold = dataframe.combined(Buy_and_hold.Historic_return(self.raw_data, self.weight))
        self.bh_return_data = returns.returns(self.buy_and_hold["Ratio"])
        self.bh_static_risk_data = static_risk.static_calc(self.buy_and_hold["Ratio"], *self.bh_return_data,
                                                           self.risk_free["Ratio"], self.benchmark["Ratio"])
        self.bh_rolling_risk_data = rolling_risk.rolling_calc(self.buy_and_hold["Ratio"], 
                                                              self.risk_free["Ratio"], self.benchmark["Ratio"])

        self.constant_weight = dataframe.combined(Constant_weight.Weighted_return(self.raw_data, self.weight))
        self.cw_return_data = returns.returns(self.constant_weight["Ratio"])
        self.cw_static_risk_data = static_risk.static_calc(self.constant_weight["Ratio"], *self.cw_return_data,
                                                           self.risk_free["Ratio"], self.benchmark["Ratio"])
        self.cw_rolling_risk_data = rolling_risk.rolling_calc(self.constant_weight["Ratio"], 
                                                              self.risk_free["Ratio"], self.benchmark["Ratio"])

        for k in self.raw_data:
            self.return_data.append(returns.returns(k["Ratio"]))

        for k in range(0, len(stocks)):
            self.risk_data.append(static_risk.static_calc(self.raw_data[k]["Ratio"], *self.return_data[k],
                                                          self.risk_free["Ratio"], self.benchmark["Ratio"]))

        for k in range(0, len(stocks)):
            self.raw_mon_close.append(self.raw_data[k]["Close"])
            self.raw_mon_return_temp.append(self.raw_data[k]["%Change"])
            self.monthly_art_mean.append(self.return_data[k][0])
            self.monthly_geo_mean.append(self.return_data[k][2])
            self.historical_VaR.append(self.risk_data[k][0])
            self.parametric_VaR.append(self.risk_data[k][1])
            self.sharpe_ratio.append(self.risk_data[k][2])
            self.sortino_ratio.append(self.risk_data[k][3])
            self.max_drawdown.append(self.risk_data[k][4])
            self.volatility.append(self.risk_data[k][5])


        for k in self.return_data:
            retirement.retirement_amount(k[2])

        self.sim_result = monte_carlo.simulation(self.raw_mon_return_temp, self.monthly_art_mean, self.stocks, self.weight, self.timeframe)
        self.bh_historical_return = self.buy_and_hold["result"]
        self.cw_historical_return = self.constant_weight["result"]

