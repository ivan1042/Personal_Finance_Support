import analysis
import plotly.express as px
from service.dataframe import *
from service.lazy_update import *

stocks = "VOO"
stocks_list = stocks.split(",")
stripped_stock = [item.strip() for item in stocks_list]
print(stripped_stock)