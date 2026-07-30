import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
from parameter import *

target = "NVDA"
interval= "1d"


df = stock_stats(target, interval)
df_VFINX = VFINX_df(interval)
st.set_page_config(layout="wide")
left, right = st.columns([1,1])

with left:
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

    fig_1.add_traces(fig_1_close.data + fig_1_top_vo.data + fig_1_top_be.data + fig_1_buttom_vo.data + fig_1_buttom_be.data)

    st.plotly_chart(
        fig_1,
        width='stretch'
    )

    st.subheader("Daily return distribution")
    fig_3 = px.histogram(df["%Change"], nbins=100)
    st.plotly_chart(fig_3,
                    width='stretch'
                    )

    st.subheader("Recent 7 years daily return distribution")
    fig_5 = px.histogram(df["%Change"].loc['2018-01-01':'2025-03-31'], nbins=100)
    st.plotly_chart(fig_5,
                    width='stretch'
                    )
with right:
    st.subheader("VOO close")

    fig_6 = px.line(df_VFINX["Close"]
                    )
    st.plotly_chart(
        fig_6,
        width='stretch'
    )

    st.subheader("%change, volatility and beta")
    df_1 = df[["%Change", "Volatility", "Beta"]].copy()
    fig_2 = px.line(df_1
                    )
    st.plotly_chart(
        fig_2,
        width='stretch'
    )

    st.subheader("Non-systematic and close chart")


    fig_4 = make_subplots(
        specs=[[{"secondary_y": True}]],
    )
    fig_4_close = px.line(df["Close"])
    fig_4_beta = px.line(df["Non-systematic"])
    fig_4_beta.update_traces(yaxis="y2", line=dict(color="orange"))

    fig_4.add_traces(fig_4_close.data + fig_4_beta.data)

    st.plotly_chart(
        fig_4,
        width='stretch'
    )