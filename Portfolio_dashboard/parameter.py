import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#from sympy.core.evalf import fastlog

import analysis
from analytics.weighted import weight

st.set_page_config(
    page_title="Parameter navigator",
    layout="wide"
)

# ---------------- Header ----------------

st.title("💰 Parameter navigator")

st.divider()

# ---------------- Main Area ----------------

left, center, right = st.columns([1,1,1])

# ==========================================
# LEFT PANEL
# ==========================================

with left:

    st.subheader("Portfolio Input")

    stocks = st.text_input(
        "Stock Tickers",
        "AAPL,BIDU"
    )

    weights = st.text_input(
        "Weights",
        "0.3,0.7"
    )

    capital = st.number_input(
        "Initial Capital",
        value = 100000
    )

    years = st.slider(
        "Investment Horizon",
        1,
        40,
        20
    )

    submit = st.button(
        "Analyze Portfolio",
        use_container_width = True
    )

if submit:
    stocks_list = stocks.split(",")
    stripped_stock = [item.strip() for item in stocks_list]
    weight_list = weights.split(",")
    stripped_weight = [float(item.strip()) for item in weight_list]

    if len(stripped_weight) != len(stripped_stock):
        st.text("Number of stock and weight does not match")
    elif sum(stripped_weight) != 1:
        st.text("Sum of weight does not equal to 1")
    elif capital <= 0:
        st.text("Capital must greater than 0")

    else:

        analyzed = analysis.analysis(stripped_stock, stripped_weight, years)


        weighted_return = weight(stripped_weight, analyzed.monthly_art_mean)
        weighted_sharpe = weight(stripped_weight, analyzed.sharpe_ratio)
        weighted_volatility = weight(stripped_weight, analyzed.volatility)
        weighted_historical_VaR = weight(stripped_weight, analyzed.historical_VaR)
        weighted_sortino_ratio = weight(stripped_weight, analyzed.sortino_ratio)
        weighted_max_drawdown = weight(stripped_weight, analyzed.max_drawdown)

        with center:

            st.subheader("Buy and hold Risk")

            st.metric("VaR", analyzed.bh_risk_data[0])

            st.metric("Max DD", analyzed.bh_risk_data[4])

            st.metric("Sortino", analyzed.bh_risk_data[3])

        with right:

            st.subheader("Fixed weight Risk")

            st.metric("VaR", weighted_historical_VaR)

            st.metric("Max DD", weighted_max_drawdown)

            st.metric("Sortino", weighted_sortino_ratio)

        st.divider()

        col_1, col_2 = st.columns([1,1])

        with col_1:
            st.subheader("BH Historical Portfolio Performance")

            fig_1 = px.line(
                analyzed.bh_historical_return * capital
            )
            st.plotly_chart(
                fig_1,
                width='stretch'
            )

            st.subheader("return maxtrix")
            st.metric("Yearly geo mean", analyzed.bh_return_data[3])
            st.metric("Historical VaR", analyzed.bh_risk_data[0])
            st.metric("Parametric VaR", analyzed.bh_risk_data[1])
            st.metric("sharpe_ratio", analyzed.bh_risk_data[2])
            st.metric("sortino_ratio", analyzed.bh_risk_data[3])
            st.metric("max_drawdown", analyzed.bh_risk_data[4])
            st.metric("volatility", analyzed.bh_risk_data[5])

        with col_2:
            st.subheader("CW Historical Portfolio Performance")
            fig_2 = px.line(
                analyzed.cw_historical_return * capital
            )
            st.plotly_chart(
                fig_2,
                width='stretch'
            )
            st.subheader("return maxtrix")
            st.metric("Yearly geo mean", analyzed.cw_return_data[3])
            st.metric("Historical VaR", analyzed.cw_risk_data[0])
            st.metric("Parametric VaR", analyzed.cw_risk_data[1])
            st.metric("sharpe_ratio", analyzed.cw_risk_data[2])
            st.metric("sortino_ratio", analyzed.cw_risk_data[3])
            st.metric("max_drawdown", analyzed.cw_risk_data[4])
            st.metric("volatility", analyzed.cw_risk_data[5])
