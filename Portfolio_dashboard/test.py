import analysis
import plotly.express as px
from service.dataframe import *
from service.lazy_update import *
from analytics.weighted import *


stripped_stock = ["AAPL", "GOOG"]
stripped_weight = [0.3, 0.7]
years = 20

analyzed = analysis.analysis(stripped_stock, stripped_weight, years)

print(analyzed.raw_data)