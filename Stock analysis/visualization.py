import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
from parameter import *


st.set_page_config(layout="wide")
left, right = st.columns([1,1])

with left:
    st.subheader("close")

    fig_1 = px.line(df["Close"]
    )
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
    st.subheader("close")

    fig_6 = px.line(df_VFINX["Close"]
                    )
    st.plotly_chart(
        fig_6,
        width='stretch'
    )

    st.subheader("%change, volatility and beta")
    df_1 = df.drop(columns=["Close", "Change", "Ratio"])
    fig_2 = px.line(df_1
                    )
    st.plotly_chart(
        fig_2,
        width='stretch'
    )

    st.subheader("Non-systematic and close chart")
    df_2 = df.drop(columns=["Change", "Ratio", "Volatility", "%Change", "Beta"])
    fig_4 = make_subplots(
        specs=[[{"secondary_y": True}]],
    )
    fig_4_close = px.line(df_2["Close"])
    fig_4_beta = px.line(df_2["Non-systematic"])
    fig_4_beta.update_traces(yaxis="y2", line=dict(color="orange"))

    fig_4.add_traces(fig_4_close.data + fig_4_beta.data)

    st.plotly_chart(
        fig_4,
        width='stretch'
    )