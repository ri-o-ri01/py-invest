import yfinance as yf
import pandas as pd

def fetch_price_history(ticker, start="2023-01-01", end=None):
    try:
        data = yf.download(ticker, start=start, end=end)
        if data is None or data.empty:
            return pd.Series(dtype=float)
        if "Adj Close" in data.columns:
            return data["Adj Close"]
        elif "Close" in data.columns:
            return data["Close"]
        else:
            return pd.Series(dtype=float)
    except Exception as e:
        print(f"[ERROR] {ticker}: {e}")
        return pd.Series(dtype=float)