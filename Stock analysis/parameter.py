import lazy_update
import matplotlib.pyplot as plt
"""stocks = ["AAPL", "VFINX"]

for stock in stocks:
    lazy_update.csv_checker(stock)
    print(lazy_update.to_dataframe(stock))

"""

df_AAPL = lazy_update.to_dataframe("AAPL")
df_VFINX = lazy_update.to_dataframe("VFINX")
df_AAPL["Volatility"] = df_AAPL['%Change'].rolling(window=36).std()
df_AAPL["Beta"] = df_AAPL["%Change"].rolling(window=36).cov(df_VFINX["%Change"]) / (df_AAPL["Volatility"]) ** 2

print(df_AAPL)
df_AAPL.drop(columns = ["Close", "Change", "Ratio"], inplace = True)
for col in df_AAPL:
    plt.plot(df_AAPL[col], label = col)
    plt.legend()
plt.show()