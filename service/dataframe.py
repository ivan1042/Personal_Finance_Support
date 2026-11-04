import pandas as pd
from pathlib import Path


def stats(stock_code = "VFINX", interval = "1mo", hk = False):
    if hk:
        data = Path(__file__).resolve().parent.parent / "data" / "hkex_to_hk_flow" / "hk_stocks"
    else:
        data = Path(__file__).resolve().parent.parent / "data"
    for item in data.iterdir():
        if f"{stock_code}_{interval}" in item.name:
            df = pd.read_csv(item, header = 0, index_col = 0, skiprows = [1, 2])
            df.index.name = "date"
    df = df.drop(columns = ["High", "Low", "Open", "Volume"])
    df["Change"] = df["Close"].diff( periods = 1)
    df["%Change"] = df["Close"].pct_change()
    df["Ratio"] = 1 + df["%Change"]

    return df

def combined(df):
    df["Change"] = df["result"].diff(periods=1)
    df["%Change"] = df["result"].pct_change()
    df["Ratio"] = 1 + df["%Change"]

    return df