import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
from parameter import *


target = ["NVDA", "AAPL", "MSFT", "GOOG", "AMZN"]
interval= "1d"
#goog, msft top beta is correct signal
def plot(df, target):
    st.subheader(f"{target} close")
    fig_1 = make_subplots()
    fig_1_close = px.line(df["Close"])
    fig_1_top_vo = px.scatter(df["Top_vo"])
    fig_1_top_be = px.scatter(df["Top_be"])
    fig_1_buttom_vo = px.scatter(df["Buttom_vo"])
    fig_1_buttom_be = px.scatter(df["Buttom_be"])
    fig_1_top_vo.update_traces(marker=dict(color="green"))
    fig_1_top_be.update_traces(marker=dict(color="red"))
    fig_1_buttom_vo.update_traces(marker=dict(color="blue"))
    fig_1_buttom_be.update_traces(marker=dict(color="orange"))

    fig_1.add_traces(
        fig_1_close.data + fig_1_top_vo.data + fig_1_top_be.data + fig_1_buttom_vo.data + fig_1_buttom_be.data)

    st.plotly_chart(
        fig_1,
        width='stretch'
    )


st.subheader(f"VFINX close")
df = stock_stats("VFINX")
fig_1 = make_subplots()
fig_1_close = px.line(df["Close"])
fig_1_top_vo = px.scatter(df["Top_vo"])
fig_1_buttom_vo = px.scatter(df["Buttom_vo"])
fig_1_top_vo.update_traces(marker=dict(color="green"))
fig_1_buttom_vo.update_traces(marker=dict(color="blue"))

fig_1.add_traces(
    fig_1_close.data + fig_1_top_vo.data + fig_1_buttom_vo.data)

st.plotly_chart(
    fig_1,
    width='stretch'
)

left, right = st.columns([1,1])
st.set_page_config(layout="wide")


for i, k in enumerate(target):
    df = stock_stats(k, interval)
    if i % 2 == 0:
        with left:
            plot(df, k)
    else:
        with right:
            plot(df, k)





