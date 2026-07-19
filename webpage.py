import streamlit as st
from dashbroad import *
import plotly.express as px

st.set_page_config(page_title = "Finance Dashboard", page_icon = ":bar_chart:", layout="wide")
st.subheader("Welcome to Finance Dashboard")
st.markdown("##", unsafe_allow_html=True)

st.dataframe(ticker_info, column_order=["Ticker", "Close", "Industry", "Summary"])
st.markdown("##", unsafe_allow_html=True)