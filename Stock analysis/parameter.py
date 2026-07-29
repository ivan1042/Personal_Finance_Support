import lazy_update
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

target = "NVDA"
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



df["Top_vo"] = None
df["Top_vo"] = np.where(
    df["Volatility"] >= df["Volatility"].quantile(0.95) ,
    df["Close"],
    df["Top_vo"],
)

df["Top_be"] = None
df["Top_be"] = np.where(
    df["Beta"] >= df["Beta"].quantile(0.95) ,
    df["Close"],
    df["Top_be"],
)

df["Buttom_vo"] = None
df["Buttom_vo"] = np.where(
    df["Volatility"] <= df["Volatility"].quantile(0.05) ,
    df["Close"],
    df["Buttom_vo"],
)

df["Buttom_be"] = None
df["Buttom_be"] = np.where(
    df["Beta"] <= df["Beta"].quantile(0.05) ,
    df["Close"],
    df["Buttom_be"],
)



