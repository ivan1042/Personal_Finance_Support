from pathlib import Path
import sys
service_root = Path(__file__).resolve().parent.parent
sys.path.append(str(service_root))
from service import yahoo
from service import dataframe

def csv_checker(stock: str, interval):
    target_path = Path(__file__).resolve().parent.parent / "data" / f"{stock}_{interval}_historical.csv"
    if target_path.exists():
        print(f"Found match:{stock}_{interval}_historical.csv")
    else:
        yahoo.get_historical_data(stock, interval)

def to_dataframe(stock: str, interval = '1mo'):

    return dataframe.stats(stock, interval)
