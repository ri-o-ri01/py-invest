from datetime import datetime
import pandas as pd

def safe_return(numerator, denominator):
    if denominator == 0 or denominator is None:
        return None
    return numerator / denominator - 1

def compute_returns_custom(data: pd.Series, start_date, end_date):
    data = data.dropna()

    latest = float(data.iloc[-1])
    prev_day = float(data.iloc[-2]) if len(data) >= 2 else latest

    # 終了値
    end_data = data[data.index <= pd.to_datetime(end_date)]
    end_val = float(end_data.iloc[-1]) if not end_data.empty else latest

    # 開始値
    start_data = data[data.index >= pd.to_datetime(start_date)]
    start_val = float(start_data.iloc[0]) if not start_data.empty else latest

    # 月初・年初
    month_start = pd.to_datetime(end_date).replace(day=1)
    year_start = pd.to_datetime(f"{end_date.year}-01-01")

    month_data = data[data.index <= month_start]
    year_val = data[data.index <= year_start]

    month_val = float(month_data.iloc[-1]) if not month_data.empty else latest
    year_val = float(year_val.iloc[-1]) if not year_val.empty else latest

    return {
        "start": start_val,
        "end": end_val,
        "latest": latest,
        "deviation": end_val / start_val - 1,  # ← 修正ここ
        "change_from_prev_day": latest / prev_day - 1,
        "change_from_month_end": latest / month_val - 1,
        "change_from_year_end": latest / year_val - 1
    }
