import lazy_update
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots

stocks = ["AAPL", "VFINX"]

for stock in stocks:
    lazy_update.csv_checker(stock)



df_AAPL = lazy_update.to_dataframe("AAPL")
df_VFINX = lazy_update.to_dataframe("VFINX")
df_AAPL["Volatility"] = df_AAPL['%Change'].rolling(window=36).std()
df_AAPL["Beta"] = df_AAPL["%Change"].rolling(window=36).cov(df_VFINX["%Change"]) / (df_AAPL["Volatility"]) ** 2

"""print(df_AAPL)
df_AAPL.drop(columns = ["Close", "Change", "Ratio"], inplace = True)
for col in df_AAPL:
    plt.plot(df_AAPL[col], label = col)
    plt.legend()
plt.show()"""

st.set_page_config(layout="wide")
left, right = st.columns([1,1])

with left:
    st.subheader("close")

    fig_1 = px.line(df_AAPL["Close"]
    )
    st.plotly_chart(
        fig_1,
        use_container_width=True,
    )

    fig_3 = px.histogram(df_AAPL["%Change"], nbins=50)
    st.plotly_chart(fig_3,
                    use_container_width=True
                    )

    fig_5 = px.histogram(df_AAPL["%Change"].loc['2018-01-01':'2025-03-31'], nbins=50)
    st.plotly_chart(fig_5,
                    use_container_width=True
                    )
with right:
    st.subheader("%change, volatility and beta")
    df_1 = df_AAPL.drop(columns=["Close", "Change", "Ratio"])
    fig_2 = px.line(df_1
                    )
    st.plotly_chart(
        fig_2,
        use_container_width=True,
    )


    df_2 = df_AAPL.drop(columns=["Change", "Ratio", "Volatility", "%Change"])
    fig_4 = make_subplots(
        specs=[[{"secondary_y": True}]],
        subplot_titles=("Monthly Revenue and Growth Rate",),
    )
    fig_4_close = px.line(df_2["Close"])
    fig_4_beta = px.line(df_2["Beta"])
    fig_4_beta.update_traces(yaxis="y2", line=dict(color="red"))

    fig_4.add_traces(fig_4_close.data + fig_4_beta.data)

    st.plotly_chart(
        fig_4,
        use_container_width=True,
    )