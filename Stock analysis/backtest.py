import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
from parameter import *

df["Signal"] = None
df["Signal"] = np.where(
    df["Top_be"] != None,
    1,
    df["Signal"],
)
df["Signal"] = np.where(
    df["Beta"] <= 0,
    -1,
    df["Signal"],
)

prev_signal = df["Signal"].shift(1)

df["Clean_signal"] = np.where(
    (df["Signal"] > 0) & (prev_signal != 1),
    df["Signal"],
    np.where(
        (df["Signal"] < 0) & (prev_signal != -1),
        df["Signal"],
        np.nan
    )
)

df["Signal"] = df["Clean_signal"]

is_buy = df["Signal"] == 1
is_sell = df["Signal"] == -1
df['Last_Buy_Idx'] = pd.Series(np.where(is_buy, df.index, np.nan), index=df.index).ffill()
df['Last_Sell_Idx'] = pd.Series(np.where(is_sell, df.index, np.nan), index=df.index).ffill()

# Valid Sell: Current row is a sell, and the last buy timestamp is newer than the last sell timestamp
# Note: Handle the initial NaN values safely using .fillna()
valid_sell = is_sell & (df['Last_Buy_Idx'] > df['Last_Sell_Idx'].fillna(pd.Timestamp.min))

# Build final clean trading signal column
df['Final_Signal'] = 0
df.loc[is_buy, 'Final_Signal'] = 1
df.loc[valid_sell, 'Final_Signal'] = -1

# Drop the temporary state tracker columns
df = df.drop(columns=['Last_Buy_Idx', 'Last_Sell_Idx'])
print(df.head())

#Second system
df["Buy"] = df["Top_be"]
prev_buy = df["Buy"].shift(1)
df["Clean_buy"] = np.where(
    (df["Buy"] > 0) & (prev_buy >= 0),
    None,
    df["Buy"],
)

df["Clean_sell"] = np.where(
    df["Beta"] <= 0 ,
    df["Close"],
    None
)


df["Sell"] = np.where(df["Signal"] == -1, df["Close"], np.nan)
clean_sells = df["Sell"].dropna()
fig_1 = make_subplots()
fig_1_close = px.line(df["Close"])
fig_1_buy = px.scatter(df["Clean_buy"])
fig_1_sell = px.scatter(df["Clean_sell"])
fig_1_buy.update_traces(marker=dict(color="green"))
fig_1_sell.update_traces(marker=dict(color="red"))

fig_1.add_traces(fig_1_close.data + fig_1_buy.data + fig_1_sell.data)

st.plotly_chart(
    fig_1,
    width='stretch'
)

