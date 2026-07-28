import lazy_update
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

target = "GOOG"
stocks = [target, "VFINX"]
interval = "1d"

for stock in stocks:
    lazy_update.csv_checker(stock, interval)



df = lazy_update.to_dataframe(target, interval)
df_VFINX = lazy_update.to_dataframe("VFINX", interval)
df["Volatility"] = df['%Change'].rolling(window=36).std()
df["Beta"] = df["%Change"].rolling(window=36).cov(df_VFINX["%Change"]) / (df["Volatility"]) ** 2


temp = df["Close"]
df.drop(columns = ["Close"], inplace = True)
df = (df - df.mean()) / df.std()
df["Close"] = temp
df["Non-systematic"] =df["Volatility"] - df["Beta"]

df["Signal"] = 0
df["Signal"] = np.where(
    (df["Beta"] > 2) ,
    1,
    df["Signal"],
)
df["Signal"] = np.where(
    (df["Beta"] <= -1) & (df["Volatility"] <= 0) ,
    -1,
    df["Signal"],
)

prev_signal = df["Signal"].shift(1)

df["Clean_signal"] = np.where(
    (df["Signal"] > 0) & (prev_signal != 1),
    df["Signal"],
    np.where(
        (df["Signal"] < 0) & (prev_signal != -1),
        df["Signal"],
        np.nan
    )
)

df["Signal"] = df["Clean_signal"]

df["Buy"] = np.where(df["Signal"] == 1, df["Close"], np.nan)
df["Sell"] = np.where(df["Signal"] == -1, df["Close"], np.nan)
clean_buys = df["Buy"].dropna()
clean_sells = df["Sell"].dropna()




