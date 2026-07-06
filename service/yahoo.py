import yfinance as yf
import datetime
import shutil
from pathlib import Path

def get_historical_data(symbol, start = None, end = datetime.date.today().strftime('%Y-%m-%d'), interval = "1mo"):
    if start == None:
        data = yf.download(symbol, period = "max", interval = interval)
    else:
        data = yf.download(symbol, start = start, end = end, interval = interval)

    data.to_csv(f"{symbol}_historical.csv")
    service = Path(__file__).resolve().parent
    file = service / f"{symbol}_historical.csv"
    target = service.parent / "data"
    shutil.move(file, target)
    return target

