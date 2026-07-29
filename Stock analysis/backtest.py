import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
from parameter import *

df["Signal"] = None
_ = """df["Signal"] = np.where(
    df["Top_be"] != None,
    1,
    df["Signal"],
)"""
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

df["Buy"] = df["Top_be"]
prev_buy = df["Buy"].shift(1)
df["Clean_buy"] = np.where(
    (df["Buy"] > 0) & (prev_buy >= 0),
    None,
    df["Buy"],
)


df["Sell"] = np.where(df["Signal"] == -1, df["Close"], np.nan)
clean_sells = df["Sell"].dropna()
fig_1 = make_subplots()
fig_1_close = px.line(df["Close"])
fig_1_buy = px.scatter(df["Clean_buy"])
fig_1_sell = px.scatter(df["Sell"])
fig_1_buy.update_traces(marker=dict(color="green"))
fig_1_sell.update_traces(marker=dict(color="red"))

fig_1.add_traces(fig_1_close.data + fig_1_buy.data + fig_1_sell.data)

st.plotly_chart(
    fig_1,
    width='stretch'
)

