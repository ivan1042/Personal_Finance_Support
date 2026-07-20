import streamlit as st
import dashbroad
import pandas as pd
import plotly.express as px

st.set_page_config(page_title = "Finance Dashboard", page_icon = ":bar_chart:", layout="wide")
st.subheader("Welcome to Finance Dashboard")
st.markdown("##", unsafe_allow_html=True)

stocks_owned = st.text_input("Enter stocks code in your portfolio e.g. AAPL, GOOG")
st.markdown("##", unsafe_allow_html=True)
stocks_weight = st.text_input("Enter the corresponding weight e.g. 0.7, 0.3")
st.markdown("##", unsafe_allow_html=True)

if st.button("Submit", key = 1):
    stocks_list = stocks_owned.split(",")
    stripped_stock = [item.strip() for item in stocks_list]
    weight_list = stocks_weight.split(",")
    stripped_weight = [float(item.strip()) for item in weight_list]
    st.success(stripped_weight)
    stocks_info = dashbroad.analysis(stripped_stock, stripped_weight)
    df_ticker_info = pd.DataFrame(stocks_info, columns=["Ticker", "Close", "Industry", "Summary"])
    df_ticker_info.set_index(df_ticker_info.columns[0], inplace=True)
    st.dataframe(df_ticker_info)
    st.markdown("##", unsafe_allow_html=True)

analysis_timeframe = st.slider("Choose a timeframe (year)", min_value=1, max_value=40)

# Display the selected level
st.write(f"Selected level: {analysis_timeframe}")
#print(dashbroad.analysis(stocks = ["VFINX", "AAPL"], weight = [0.7, 0.3]))