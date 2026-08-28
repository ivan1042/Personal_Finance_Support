from service import lazy_update
from service import dataframe

def test_helper():
    stocks = ["AAPL", "BIDU"]
    weight = [0.7, 0.3]
    raw_data = []

    for stock in stocks:
        lazy_update.csv_checker(stock, "1mo")
        raw_data.append(dataframe.stats(stock))

    return raw_data