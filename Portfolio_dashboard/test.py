import analysis
import plotly.express as px
from service.dataframe import *
from service.lazy_update import *
from analytics.weighted import *


stripped_stock = ["AAPL", "GOOG"]
stripped_weight = [0.3, 0.7]
years = 20

analyzed = analysis.analysis(stripped_stock, stripped_weight, years)

            # Metrics
weighted_return = weight(stripped_weight, analyzed.monthly_art_mean)
weighted_sharpe = weight(stripped_weight, analyzed.sharpe_ratio)
weighted_volatility = weight(stripped_weight, analyzed.volatility)
weighted_historical_VaR = weight(stripped_weight, analyzed.historical_VaR)
weighted_sortino_ratio = weight(stripped_weight, analyzed.sortino_ratio)
weighted_max_drawdown = weight(stripped_weight, analyzed.max_drawdown)
print(weighted_max_drawdown)