import yfinance as yf
import datetime
import shutil
from pathlib import Path

def get_historical_data(symbol, interval = "1mo", start = None, end = datetime.date.today().strftime('%Y-%m-%d')):
    if start == None:
        data = yf.download(symbol, period = "max", interval = interval)
    else:
        data = yf.download(symbol, start = start, end = end, interval = interval)

    service = Path(__file__).resolve().parent
    target_folder = service.parent / "data"
    target_folder.mkdir(parents = True, exist_ok = True)
    target_file = target_folder / f"{symbol}_{interval}_historical.csv"
    data.to_csv(target_file)

    return

