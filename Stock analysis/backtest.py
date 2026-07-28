import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
from parameter import *

fig_1 = make_subplots()
fig_1_close = px.line(df["Close"])
fig_1_buy = px.scatter(df["Buy"])
fig_1_sell = px.scatter(df["Sell"])
fig_1_buy.update_traces(marker=dict(color="green"))
fig_1_sell.update_traces(marker=dict(color="red"))

fig_1.add_traces(fig_1_close.data + fig_1_buy.data + fig_1_sell.data)

st.plotly_chart(
    fig_1,
    width='stretch'
)