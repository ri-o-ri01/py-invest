from datetime import datetime
import pandas as pd

def compute_returns(data: pd.Series):
    latest = float(data.iloc[-1])
    prev_day = float(data.iloc[-2])
    month_end = float(data[data.index <= str(datetime.now().replace(day=1))].iloc[-1])
    year_end = float(data[data.index <= f"{datetime.now().year - 1}-12-31"].iloc[-1])
    
    return {
        "latest": latest,
        "change_from_prev_day": latest / prev_day - 1,
        "change_from_month_end": latest / month_end - 1,
        "change_from_year_end": latest / year_end - 1
    }
