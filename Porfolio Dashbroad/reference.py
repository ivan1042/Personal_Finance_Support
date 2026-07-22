import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dashbroad

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
    weighted_return = sum(x * y for x, y in zip(stripped_weight, dashbroad.analysis().art_return_temp))
    st.metric("Expected Return", f"{weighted_return:.2%}")
    st.metric("Sharpe", f"{analyzed.sharpe:.2f}")

    # Charts
    st.plotly_chart(analyzed.allocation_chart)
    st.plotly_chart(analyzed.mc_chart)
    st.plotly_chart(analyzed.history_chart)

# ==========================================
# RIGHT PANEL
# ==========================================

    with right:

        st.subheader("Portfolio Summary")

        metric1, metric2, metric3 = st.columns(3)

        metric1.metric(
            "Expected Return",
            "12.3%"
        )

        metric2.metric(
            "Volatility",
            "18.1%"
        )

        metric3.metric(
            "Sharpe",
            "1.04"
        )

        st.info(
            """
            Portfolio description will appear here.
    
            Company information
    
            Sector Allocation
    
            Market Cap
    
            Investment Thesis
            """
        )

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

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                y=[100,103,105,109,115],
                mode="lines"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ---------------- Risk ----------------

    with risk_col:

        st.subheader("Risk")

        st.metric("VaR", "-6.2%")

        st.metric("Max DD", "-18%")

        st.metric("Sortino", "1.38")

    st.divider()

    # ==========================================
    # Bottom Chart
    # ==========================================

    st.subheader("Historical Portfolio Performance")

    price = pd.DataFrame({
        "Date": pd.date_range("2024-01-01", periods=20),
        "Value":[100+i*2 for i in range(20)]
    })

    fig = px.line(
        price,
        x="Date",
        y="Value"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

