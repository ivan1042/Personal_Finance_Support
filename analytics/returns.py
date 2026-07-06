import pandas as pd
from pathlib import Path

current = Path(__file__).resolve().parent
data = current.parent / "data"
for item in data.iterdir():
    if "historical" in item.name:
        df = pd.read_csv(item, header = 0, index_col = 0, skiprows = [1, 2])
        df.index.name = "date"

print(df.head())