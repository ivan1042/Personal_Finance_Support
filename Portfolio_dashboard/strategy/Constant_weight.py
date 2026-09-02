import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

def Weighted_return(raw_data: list, initial_weight = [0.3, 0.7]):
    df = pd.DataFrame()
    for i, j in enumerate(raw_data):
        df[f"Ratio_{i}"] = j["Ratio"]
    df.dropna(inplace=True)
    for i, j in enumerate(raw_data):
        df[f"Cum_Ratio_{i}"] = df[f"Ratio_{i}"].shift(-1).cumprod()
    for i, j in enumerate(initial_weight):
        df[f"Weight_{i}"] = j
    for k in range(0, len(initial_weight)):
        df[f"raw_{k}"] = initial_weight[k] * df[f"Cum_Ratio_{k}"]
        df[f"New_{k}"] = df[f"Ratio_{k}"] * df[f"Weight_{k}"]
    df["raw"] = df[[f"raw_{k}" for k in range(0, len(initial_weight))]].sum(axis=1)
    df["new"] = df[[f"New_{k}" for k in range(0, len(initial_weight))]].sum(axis=1)
    df.iat[0, df.columns.get_loc("new")] = 1
    df["result"] = df["new"].cumprod()
    df.iat[0, df.columns.get_loc("result")] = 1
    df.dropna(inplace = True)

    return df

