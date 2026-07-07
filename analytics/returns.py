import pandas as pd
from pathlib import Path

current = Path(__file__).resolve().parent
data = current.parent / "data"
for item in data.iterdir():
    if "VFINX_historical" in item.name:
        df = pd.read_csv(item, header = 0, index_col = 0, skiprows = [1, 2])
        df.index.name = "date"


df = df.drop(columns = ["High", "Low", "Volume"])
df["Change"] = df["Close"] - df["Open"]
df["%Change"] = df["Change"] / df["Open"]
df["Ratio"] = 1 + df["%Change"]
