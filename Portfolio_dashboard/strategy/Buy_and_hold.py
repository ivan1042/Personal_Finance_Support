import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

def Historic_return(raw_data: list, initial_weight = [0.3, 0.7]):
    weight = pd.DataFrame()
    for i, j in enumerate(raw_data):
        weight[f"Ratio_{i}"] = j["Ratio"]
    weight.dropna(inplace=True)
    for i, j in enumerate(raw_data):
        weight[f"Cum_Ratio_{i}"] = weight[f"Ratio_{i}"].shift(-1).cumprod()

    weight.reset_index(inplace=True)
    temp = pd.DataFrame([initial_weight], columns = [f"weight_{k}" for k in range(0, len(initial_weight))])
    df = pd.concat([weight, temp], axis=1)
    df.set_index(df["date"], inplace=True)
    for k in range(0, len(initial_weight)):
        df[f"raw_{k}"] = initial_weight[k] * df[f"Cum_Ratio_{k}"].shift(1)
    df["raw"] = df[[f"raw_{k}" for k in range(0, len(initial_weight))]].sum(axis=1)
    for k in range(0, len(initial_weight)):
        df[f"New_weight_{k}"] = df[f"raw_{k}"] / df["raw"]
        df[f"New_weight_{k}"] = df[f"New_weight_{k}"].fillna(df[f"weight_{k}"])
        target = [f"New_weight_{k}" for k in range(0, len(initial_weight))]
        df[f"New_{k}"] = df[f"Ratio_{k}"] * df[f"New_weight_{k}"].shift(1)
    df["new"] = df[[f"New_{k}" for k in range(0, len(initial_weight))]].sum(axis=1)
    df.iat[0, df.columns.get_loc("new")] = 1
    df["result"] = df["new"].cumprod()
    df.iat[0, df.columns.get_loc("result")] = 1
    target.append("result")
    result = df[target]

    return result

