import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#from sympy.core.evalf import fastlog

import dashbroad
from analytics.weighted import weight

st.set_page_config(
    page_title="Personal Finance Support",
    layout="wide"
)

# ---------------- Header ----------------

st.title("💰 Personal Finance Support")
st.caption("Portfolio Analysis & Retirement Planning")

st.divider()

# ---------------- Main Area ----------------

left, right = st.columns([1,2])

# ==========================================
# LEFT PANEL
# ==========================================

with left:

    st.subheader("Portfolio Input")

    stocks = st.text_input(
        "Stock Tickers",
        "AAPL,GOOG"
    )

    weights = st.text_input(
        "Weights",
        "0.7,0.3"
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
    analyzed = dashbroad.analysis(stripped_stock, stripped_weight, years)

    # Metrics
    weighted_return = weight(stripped_weight, dashbroad.analysis().monthly_art_mean)
    weighted_sharpe = weight(stripped_weight, dashbroad.analysis().sharpe_ratio)
    weighted_volatility = weight(stripped_weight, dashbroad.analysis().volatility)
    weighted_historical_VaR = weight(stripped_weight, dashbroad.analysis().historical_VaR)
    weighted_sortino_ratio = weight(stripped_weight, dashbroad.analysis().sortino_ratio)
    weighted_max_drawdown = weight(stripped_weight, dashbroad.analysis().max_drawdown)
    st.metric("Expected Monthly Return", f"{(weighted_return - 1):.2%}")
    st.metric("Sharpe", f"{weighted_sharpe:.2f}")

    # Charts
#    st.plotly_chart(analyzed.allocation_chart)
#    st.plotly_chart(analyzed.mc_chart)
#    st.plotly_chart(analyzed.history_chart)

# ==========================================
# RIGHT PANEL
# ==========================================

    with right:

        st.subheader("Portfolio Summary")

        metric1, metric2, metric3 = st.columns(3)

        metric1.metric(
            "Expected Return",
            weighted_return
        )

        metric2.metric(
            "Volatility",
            weighted_volatility
        )

        metric3.metric(
            "Sharpe",
            weighted_sharpe
        )

        df_ticker_info = pd.DataFrame(dashbroad.analysis().ticker_info, columns=["Ticker", "Close", "Industry", "Summary"])
        df_ticker_info.set_index(df_ticker_info.columns[0], inplace=True)
        st.dataframe(df_ticker_info)

    # ==========================================
    # Charts
    # ==========================================

    pie_col, mc_col, risk_col = st.columns([1,2,1])

    # ---------------- Pie ----------------

    with pie_col:

        st.subheader("Allocation")

        fig = px.pie(
            names = stripped_stock,
            values = stripped_weight
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ---------------- Monte Carlo ----------------

    with mc_col:

        st.subheader("Monte Carlo")

        fig = px.line(
                dashbroad.analysis().sim_result
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ---------------- Risk ----------------

    with risk_col:

        st.subheader("Risk")

        st.metric("VaR", weighted_historical_VaR)

        st.metric("Max DD", weighted_max_drawdown)

        st.metric("Sortino", weighted_sortino_ratio)

    st.divider()

    # ==========================================
    # Bottom Chart
    # ==========================================

    st.subheader("Historical Portfolio Performance")


    fig = px.line(
        dashbroad.analysis().historical_return,
        x = "index",
        y = "%Change"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

