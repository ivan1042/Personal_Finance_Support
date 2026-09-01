import streamlit as st
import pandas as pd
import plotly.express as px
import analysis


st.set_page_config(page_title="Portfolio Risk Engine", layout="wide")
st.title("Portfolio Risk Engine")
st.caption("Portfolio strategy comparison and rolling-risk analysis")

# Desktop input row
input_1, input_2, input_3, input_4, input_5, input_6 = st.columns([1.4, 1.1, 1, 0.9, 0.9, 1])
with input_1:
    tickers = st.text_input("Tickers", "AAPL, BIDU")
with input_2:
    weights = st.text_input("Target weights", "0.3, 0.7")
with input_3:
    capital = st.number_input("Initial capital", min_value=1.0, value=100000.0)
with input_4:
    years = st.slider("Investment horizon", 1, 40, 20)
with input_5:
    rolling_window = st.selectbox("Rolling window", [36], format_func=lambda value: f"{value} months")
with input_6:
    st.write("")
    submit = st.button("Analyze portfolio", use_container_width=True, type="primary")


def risk_table(analyzed):
    """Create a comparison table from portfolio-level static risk calculations."""
    return pd.DataFrame(
        {
            "Buy & Hold": analyzed.bh_static_risk_data,
            "Constant Weight": analyzed.cw_static_risk_data,
        },
        index=[
            "Historical VaR (95%)", "Parametric VaR (95%)", "Sharpe ratio",
            "Sortino ratio", "Maximum drawdown", "Monthly volatility",
        ],
    )


if submit:
    try:
        stocks = [ticker.strip().upper() for ticker in tickers.split(",") if ticker.strip()]
        target_weights = [float(value.strip()) for value in weights.split(",")]

        if len(stocks) != len(target_weights):
            st.error("The number of tickers must match the number of weights.")
            st.stop()
        if not abs(sum(target_weights) - 1) < 1e-8:
            st.error("Target weights must sum to 1.00.")
            st.stop()

        analyzed = analysis.analysis(stocks, target_weights, years)

        st.divider()
        strategy = st.radio(
            "Strategy view", ["Compare both", "Buy & Hold", "Constant Weight"],
            horizontal=True, label_visibility="collapsed"
        )

        # KPIs use the selected portfolio strategy, never weighted individual-asset risk.
        selected_risk = (
            analyzed.bh_static_risk_data
            if strategy == "Buy & Hold"
            else analyzed.cw_static_risk_data
        )
        selected_return = (
            analyzed.bh_return_data[3] - 1
            if strategy == "Buy & Hold"
            else analyzed.cw_return_data[3] - 1
        )
        k1, k2, k3, k4, k5, k6 = st.columns(6)
        k1.metric("Annualized return", f"{selected_return:.2%}")
        k2.metric("Monthly volatility", f"{selected_risk[5]:.2%}")
        k3.metric("Sharpe ratio", f"{selected_risk[2]:.2f}")
        k4.metric("Sortino ratio", f"{selected_risk[3]:.2f}")
        k5.metric("1-month 95% VaR", f"{selected_risk[0]:.2%}", f"${selected_risk[0] * capital:,.0f}")
        k6.metric("Maximum drawdown", f"{selected_risk[4]:.2%}")

        left, right = st.columns([1.7, 1])
        with left:
            st.subheader("Historical portfolio value")
            wealth = pd.concat(
                [analyzed.bh_historical_return.rename("Buy & Hold"),
                 analyzed.cw_historical_return.rename("Constant Weight")], axis=1
            ) * capital
            if strategy == "Buy & Hold":
                wealth = wealth[["Buy & Hold"]]
            elif strategy == "Constant Weight":
                wealth = wealth[["Constant Weight"]]
            st.plotly_chart(px.line(wealth, labels={"value": "Portfolio value ($)", "index": "Date"}), use_container_width=True)

        with right:
            st.subheader("Strategy comparison")
            comparison = risk_table(analyzed)
            percentage_rows = [
                "Historical VaR (95%)", "Parametric VaR (95%)",
                "Maximum drawdown", "Monthly volatility",
            ]
            ratio_rows = ["Sharpe ratio", "Sortino ratio"]
            formatted_comparison = (
                comparison.style
                .format("{:.2%}", subset=pd.IndexSlice[percentage_rows, :])
                .format("{:.2f}", subset=pd.IndexSlice[ratio_rows, :])
            )
            st.dataframe(formatted_comparison, use_container_width=True)

        rolling_left, rolling_right = st.columns([1.55, 1])
        with rolling_left:
            st.subheader("Rolling risk monitor")
            metric = st.selectbox("Rolling metric", [
                "historical_VaR", "parametric_VaR", "volatility", "Beta",
                "sharpe_ratio", "sortino_ratio", "max_drawdown",
            ])
            rolling = pd.concat([
                analyzed.bh_rolling_risk_data[metric].rename("Buy & Hold"),
                analyzed.cw_rolling_risk_data[metric].rename("Constant Weight"),
            ], axis=1)
            st.plotly_chart(px.line(rolling, labels={"value": metric, "index": "Date"}), use_container_width=True)

        with rolling_right:
            st.subheader("Weight behavior")
            st.caption("Buy & Hold drifts; Constant Weight is rebalanced to target weights.")
            drift = analyzed.buy_and_hold[f"New_weight_{k}" for k in range(0, len(stocks))]
            for i, j in enumerate(stocks):
                drift.rename(columns = {f"New_weight_{i}": j})
            st.plotly_chart(px.line(drift, labels={"value": "Portfolio weight", "index": "Date"}), use_container_width=True)

        with st.expander("Holdings and methodology"):
            allocation = pd.DataFrame({"Ticker": stocks, "Target weight": target_weights})
            st.dataframe(allocation.style.format({"Target weight": "{:.2%}"}), use_container_width=True)
            st.caption(f"Rolling metrics use a {rolling_window}-month window. VaR confidence level: 95%.")

    except (ValueError, KeyError) as error:
        st.error(f"Unable to analyze the portfolio: {error}")