import yfinance as yf
import pandas as pd

def fetch_price_history(ticker, start="2023-01-01"):
    try:
        data = yf.download(ticker, start=start)
    except Exception as e:
        print(f"[ERROR] Failed to download {ticker}: {e}")
        return pd.Series(dtype=float)

    if data is None or not isinstance(data, pd.DataFrame):
        print(f"[ERROR] Invalid data for {ticker} (None or wrong type)")
        return pd.Series(dtype=float)

    if data.empty:
        print(f"[WARN] No data for ticker: {ticker}")
        return pd.Series(dtype=float)

    # 'Adj Close' or 'Close'
    if "Adj Close" in data.columns:
        return data["Adj Close"]
    elif "Close" in data.columns:
        print(f"[INFO] 'Adj Close' not found, using 'Close' instead for {ticker}")
        return data["Close"]
    else:
        print(f"[ERROR] No usable price columns in {ticker}")
        return pd.Series(dtype=float)