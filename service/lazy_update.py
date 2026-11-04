from pathlib import Path
import sys
service_root = Path(__file__).resolve().parent.parent
sys.path.append(str(service_root))
from service import yahoo
from service import dataframe

def csv_checker(stock: str, interval, hk = False):

    if hk:
        target_path = (Path(__file__).resolve().parent.parent / "data" / "hkex_to_hk_flow" / "hk_stocks" / f"{stock}_{interval}_historical.csv")
    else:
        target_path = Path(__file__).resolve().parent.parent / "data" / f"{stock}_{interval}_historical.csv"
    if target_path.exists():
        print(f"Found match:{stock}_{interval}_historical.csv")
        return True
    else:
        yahoo.get_historical_data(stock, interval, hk)

def to_dataframe(stock: str, interval = '1mo'):

    return dataframe.stats(stock, interval)
