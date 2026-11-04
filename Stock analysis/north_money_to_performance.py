from pathlib import Path
import sys
service_root = Path(__file__).resolve().parent.parent
sys.path.append(str(service_root))
import pandas as pd
from service import dataframe, lazy_update
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
from service  import yahoo


col = 27
location = Path(__file__).resolve().parent.parent / "data" / "hkex_to_hk_flow"
df = pd.read_csv(location / "parsed_updated.csv", index_col=0)
stock = df.columns[col]
code = f"{str(stock).zfill(4)}.HK"
check = lazy_update.csv_checker(code, "1d", hk = True)
if check:
    pass
else:
    yahoo.get_historical_data(code, "1d", hk = True, start = "2025-12-31")
quote = dataframe.stats(stock_code = code , interval = "1d", hk = True)
new_df = df[[stock]].copy()

new_df["%Change"] = new_df[str(stock)].pct_change()
new_df["Ratio"] = 1 + new_df["%Change"]
new_df["Cum_Ratio"] = new_df["Ratio"].cumprod()
quote = quote.sort_index()
new_df = new_df.sort_index()

fig_4 = make_subplots(
        specs=[[{"secondary_y": True}]],
    )
fig_4_close = px.line(quote["Close"])
fig_4_beta = px.line(new_df["Cum_Ratio"])
fig_4_beta.update_traces(yaxis="y2", line=dict(color="orange"))

fig_4.add_traces(fig_4_close.data + fig_4_beta.data)

st.plotly_chart(
    fig_4,
    width='stretch'
)