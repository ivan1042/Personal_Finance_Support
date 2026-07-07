import pandas as pd
from pathlib import Path
from scipy.stats import gmean

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

monthly_art_mean = df["Ratio"].mean()
yearly_art_mean = monthly_art_mean**12-1
monthly_geo_mean = gmean(df["Ratio"])
yearly_geo_mean = monthly_geo_mean**12-1


