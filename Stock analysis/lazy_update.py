from pathlib import Path
import sys
service_root = Path(__file__).resolve().parent.parent
sys.path.append(str(service_root))
from service import yahoo
from service import dataframe

def csv_checker(stock: str):
    target_path = Path(__file__).resolve().parent.parent / "data" / f"{stock}_historical.csv"
    if target_path.exists():
        print(f"Found match:{stock}_historical.csv")
    else:
        yahoo.get_historical_data(stock)

def to_dataframe(stock: str):

    return dataframe.stats(stock)
