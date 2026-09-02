"""Desktop Streamlit dashboard for the portfolio risk engine.

Run from the Portfolio_dashboard directory:
    streamlit run webpage.py
"""

import pandas as pd
import plotly.express as px
import streamlit as st

import analysis


st.set_page_config(page_title="Portfolio Risk Engine", layout="wide")


STATIC_RISK_ROWS = [
    "Historical VaR (95%)",
    "Parametric VaR (95%)",
    "Sharpe ratio",
    "Sortino ratio",
    "Maximum drawdown",
    "Monthly volatility",
]
PERCENTAGE_RISK_ROWS = [
    "Historical VaR (95%)",
    "Parametric VaR (95%)",
    "Maximum drawdown",
    "Monthly volatility",
]
RATIO_RISK_ROWS = ["Sharpe ratio", "Sortino ratio"]
ROLLING_METRICS = {
    "Historical VaR (95%)": "historical_VaR",
    "Parametric VaR (95%)": "parametric_VaR",
    "Volatility": "volatility",
    "Beta": "Beta",
    "Sharpe ratio": "sharpe_ratio",
    "Sortino ratio": "sortino_ratio",
    "Maximum drawdown": "max_drawdown",
}


def parse_portfolio(ticker_text: str, weight_text: str) -> tuple[list[str], list[float]]:
    """Parse and validate user-entered tickers and target weights."""
    tickers = [ticker.strip().upper() for ticker in ticker_text.split(",") if ticker.strip()]
    weights = [float(value.strip()) for value in weight_text.split(",") if value.strip()]

    if not tickers:
        raise ValueError("Enter at least one ticker.")
    if len(tickers) != len(weights):
        raise ValueError("The number of tickers must equal the number of target weights.")
    if any(weight < 0 for weight in weights):
        raise ValueError("Target weights cannot be negative.")
    if not abs(sum(weights) - 1.0) < 1e-8:
        raise ValueError("Target weights must sum to 1.00.")

    return tickers, weights


def static_risk_comparison(analyzed) -> pd.DataFrame:
    """Return static risk metrics for the two portfolio strategies."""
    return pd.DataFrame(
        {
            "Buy & Hold": analyzed.bh_static_risk_data,
            "Constant Weight": analyzed.cw_static_risk_data,
        },
        index=STATIC_RISK_ROWS,
    )


def format_risk_table(data: pd.DataFrame):
    """Apply percentage formatting only to percentage-based risk measures."""
    return (
        data.style
        .format("{:.2%}", subset=pd.IndexSlice[PERCENTAGE_RISK_ROWS, :])
        .format("{:.2f}", subset=pd.IndexSlice[RATIO_RISK_ROWS, :])
    )


def strategy_data(analyzed, strategy_name: str):
    """Return return metrics, risk metrics, and wealth series for one strategy."""
    if strategy_name == "Buy & Hold":
        return (
            analyzed.bh_return_data,
            analyzed.bh_static_risk_data,
            analyzed.bh_historical_return,
        )
    return (
        analyzed.cw_return_data,
        analyzed.cw_static_risk_data,
        analyzed.cw_historical_return,
    )


def display_kpis(analyzed, strategy_name: str, capital: float) -> None:
    """Display clearly labelled KPI cards for exactly one strategy."""
    return_data, risk_data, _ = strategy_data(analyzed, strategy_name)
    st.subheader(f"Key metrics — {strategy_name}")
    st.caption("Static metrics are calculated from the portfolio return series.")

    annual_return = return_data[3] - 1
    historical_var, _, sharpe, sortino, max_drawdown, volatility = risk_data
    cards = st.columns(6)
    cards[0].metric("Annualized geometric return", f"{annual_return:.2%}")
    cards[1].metric("Monthly volatility", f"{volatility:.2%}")
    cards[2].metric("Sharpe ratio", f"{sharpe:.2f}")
    cards[3].metric("Sortino ratio", f"{sortino:.2f}")
    cards[4].metric("1-month 95% Historical VaR", f"{historical_var:.2%}", f"${historical_var * capital:,.0f}")
    cards[5].metric("Maximum drawdown", f"{max_drawdown:.2%}")


# Persist the completed analysis across widget interactions. Without this,
# Streamlit's normal rerun on selectbox changes would clear the dashboard.
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "portfolio_config" not in st.session_state:
    st.session_state.portfolio_config = None


st.title("Portfolio Risk Engine")
st.caption("Compare Buy & Hold with Monthly-Rebalanced Constant Weight portfolios")

with st.form("portfolio_input", border=False):
    c1, c2, c3, c4, c5, c6 = st.columns([1.35, 1.1, 1, 0.85, 0.85, 1])
    with c1:
        ticker_text = st.text_input("Tickers", "AAPL, BIDU")
    with c2:
        weight_text = st.text_input("Target weights", "0.30, 0.70")
    with c3:
        capital = st.number_input("Initial capital", min_value=1.0, value=100000.0, step=1000.0)
    with c4:
        years = st.slider("Monte Carlo horizon", min_value=1, max_value=40, value=20)
    with c5:
        rolling_window = st.selectbox("Rolling window", [36], format_func=lambda months: f"{months} months")
    with c6:
        st.write("")
        submitted = st.form_submit_button("Analyze portfolio", width='stretch', type="primary")

if submitted:
    try:
        tickers, target_weights = parse_portfolio(ticker_text, weight_text)
        with st.spinner("Downloading data and calculating portfolio risk..."):
            st.session_state.analysis_result = analysis.analysis(tickers, target_weights, years)
            st.session_state.portfolio_config = {
                "tickers": tickers,
                "weights": target_weights,
                "capital": capital,
                "years": years,
                "rolling_window": rolling_window,
            }
    except (ValueError, KeyError) as error:
        st.error(f"Unable to analyze this portfolio: {error}")

if st.session_state.analysis_result is None:
    st.info("Enter a portfolio and select Analyze portfolio to view the dashboard.")
    st.stop()

analyzed = st.session_state.analysis_result
config = st.session_state.portfolio_config
capital = config["capital"]

st.divider()

# This control changes only presentation. The stored calculation stays intact.
kpi_strategy = st.radio(
    "KPI strategy",
    ["Buy & Hold", "Constant Weight"],
    horizontal=True,
    help="Choose which strategy supplies the KPI cards below.",
)
display_kpis(analyzed, kpi_strategy, capital)

st.divider()

performance_col, comparison_col = st.columns([1.7, 1])
with performance_col:
    st.subheader("Historical portfolio value")
    st.caption("Both lines use the same initial capital and the actual strategy return series.")
    wealth = pd.concat(
        [
            analyzed.bh_historical_return.rename("Buy & Hold"),
            analyzed.cw_historical_return.rename("Monthly-Rebalanced Constant Weight"),
        ],
        axis=1,
    ) * capital
    st.plotly_chart(
        px.line(wealth, labels={"value": "Portfolio value ($)", "index": "Date"}),
        width='stretch',
    )

with comparison_col:
    st.subheader("Static risk comparison")
    st.caption("Monthly portfolio return metrics.")
    st.dataframe(format_risk_table(static_risk_comparison(analyzed)), use_container_width=True)

rolling_col, weights_col = st.columns([1.55, 1])
with rolling_col:
    st.subheader("Rolling risk monitor")
    selected_label = st.selectbox("Metric", list(ROLLING_METRICS))
    selected_metric = ROLLING_METRICS[selected_label]

    rolling_data = pd.concat(
        [
            analyzed.bh_rolling_risk_data[selected_metric].rename("Buy & Hold"),
            analyzed.cw_rolling_risk_data[selected_metric].rename("Monthly-Rebalanced Constant Weight"),
        ],
        axis=1,
    )
    st.plotly_chart(
        px.line(rolling_data, labels={"value": selected_label, "index": "Date"}),
        width='stretch',
    )
    st.caption(f"{config['rolling_window']}-month window. Changing this metric does not rerun portfolio analysis.")

with weights_col:
    st.subheader("Buy & Hold weight drift")
    st.caption(
        "Asset weights vary as relative prices change. "
        "Constant Weight restores target weights every month."
    )
    weight_columns = [f"New_weight_{i}"for i in range(len(config["tickers"]))]
    drift = analyzed.buy_and_hold.loc[:, weight_columns].copy()
    drift = drift.rename(columns=dict(zip(weight_columns, config["tickers"])))
    st.plotly_chart(
        px.line(
            drift,
            labels={
                "value": "Portfolio weight",
                "index": "Date",
                "variable": "Ticker",
            },
        ),
        width='stretch',
    )

st.divider()
simulation_col, holdings_col = st.columns([1.7, 1])

with simulation_col:
    st.subheader("Monte Carlo simulation")
    st.caption(f"{config['years']}-year simulated portfolio paths based on the selected assets.")
    st.plotly_chart(
        px.line(analyzed.sim_result, labels={"value": "Portfolio value", "index": "Month"}),
        width='stretch',
    )

with holdings_col:
    st.subheader("Target allocation")
    allocation = pd.DataFrame({"Ticker": config["tickers"], "Target weight": config["weights"]})
    st.plotly_chart(px.pie(allocation, names="Ticker", values="Target weight", hole=0.45), width='stretch')
    st.dataframe(allocation.style.format({"Target weight": "{:.2%}"}), hide_index=True, width='stretch')

with st.expander("Methodology and data notes"):
    st.markdown(
        """
        - **Buy & Hold** lets allocations drift as asset prices change.
        - **Monthly-Rebalanced Constant Weight** applies the target weights to every monthly return.
        - Historical and parametric VaR use a 95% confidence level in the current risk module.
        - The `Monte Carlo horizon` input controls simulation length; historical strategy charts use all available downloaded monthly data.
        """
    )