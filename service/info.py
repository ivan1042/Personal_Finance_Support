import yfinance as yf
import pandas as pd


def ticker_info(ticker = "MSFT"):

    dat = yf.Ticker(ticker)
    dic = dat.info
    try:
        result = [ticker, dic['regularMarketPreviousClose'], dic['industry'], dic['longBusinessSummary']]
    except KeyError:
        result = [ticker, dic['regularMarketPreviousClose'], 'null', dic['longBusinessSummary']]

    return result

