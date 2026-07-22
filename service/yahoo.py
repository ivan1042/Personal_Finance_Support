import yfinance as yf
import datetime
import shutil
from pathlib import Path

def get_historical_data(symbol, start = None, end = datetime.date.today().strftime('%Y-%m-%d'), interval = "1mo"):
    if start == None:
        data = yf.download(symbol, period = "max", interval = interval)
    else:
        data = yf.download(symbol, start = start, end = end, interval = interval)

    service = Path(__file__).resolve().parent
    file = service / f"{symbol}_historical.csv"
    target_folder = service.parent / "data"
    target_folder.mkdir(parents = True, exist_ok = True)
    target_file = target_folder / f"{symbol}_historical.csv"
    data.to_csv(target_file)
    return target_folder

