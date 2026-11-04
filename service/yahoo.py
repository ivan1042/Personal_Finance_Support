import yfinance as yf
import datetime
import shutil
from pathlib import Path

def get_historical_data(symbol, interval = "1mo", hk = False, start = None, end = datetime.date.today().strftime('%Y-%m-%d')):
    if start == None:
        data = yf.download(symbol, period = "max", interval = interval)
    else:
        data = yf.download(symbol, start = start, end = end, interval = interval)

    if hk:
        target_folder = Path(__file__).resolve().parent.parent / "data" / "hkex_to_hk_flow" / "hk_stocks"
    else:
        target_folder = Path(__file__).resolve().parent.parent / "data"

    target_folder.mkdir(parents = True, exist_ok = True)
    target_file = target_folder / f"{symbol}_{interval}_historical.csv"
    data.to_csv(target_file)

    return

