import streamlit as st
from data_fetcher import fetch_price_history
from metrics import compute_returns

st.title("マーケットダッシュボード")

CATEGORY_TICKERS = {
    "株式指数": {
        "G7": {
            "日経平均": "^N225",
            "TOPIX": "^TOPX",
            "DAX": "^GDAXI",
            "S&P500": "^GSPC"
        },
        "BRICS": {
            "上海総合": "000001.SS",
            "インドSENSEX": "^BSESN"
        }
    },
    "米国株": {
        "BIG TECH": {
            "Apple": "AAPL",
            "Google": "GOOGL"
        }
    }
}

category = st.selectbox("カテゴリを選択", list(CATEGORY_TICKERS.keys()))
option = st.selectbox("銘柄を選択", list(CATEGORY_TICKERS[category].keys()))

ticker = CATEGORY_TICKERS[category][option]
data = fetch_price_history(ticker)
metrics = compute_returns(data)

st.subheader(f"{option}（{ticker}）のリターン")
st.write(f"最新価格: {metrics['latest']:.2f}")
st.write(f"前日比: {metrics['change_from_prev_day'] * 100:.2f}%")
st.write(f"前月末比: {metrics['change_from_month_end'] * 100:.2f}%")
st.write(f"前年末比: {metrics['change_from_year_end'] * 100:.2f}%")
