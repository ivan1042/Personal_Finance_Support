import streamlit as st
from dashbroad import *
import plotly.express as px

st.set_page_config(page_title = "Finance Dashboard", page_icon = ":bar_chart:", layout="wide")
st.subheader("Welcome to Finance Dashboard")
st.markdown("##", unsafe_allow_html=True)

df_ticker_info = pd.DataFrame(ticker_info, columns=["Ticker", "Close", "Industry", "Summary"])
df_ticker_info.set_index(df_ticker_info.columns[0], inplace=True)
st.dataframe(df_ticker_info)
st.markdown("##", unsafe_allow_html=True)