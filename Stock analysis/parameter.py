import lazy_update

stocks = ["AAPL", "VFINX"]

for stock in stocks:
    lazy_update.csv_checker(stock)
    print(lazy_update.to_dataframe(stock))

