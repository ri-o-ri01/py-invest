import streamlit as st
import sys
import os

# プロジェクトルートを sys.path に追加（←ここが超重要）
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from apps.market_dashboard.data_fetcher import fetch_price_history
from apps.market_dashboard.metrics import compute_returns
from apps.market_dashboard.config import CATEGORY_TICKERS

st.set_page_config(page_title="Market Dashboard", layout="wide")
st.title("📈 市況モニターダッシュボード")

# ユーザー選択
category = st.selectbox("カテゴリを選択", list(CATEGORY_TICKERS.keys()))
option = st.selectbox("銘柄を選択", list(CATEGORY_TICKERS[category].keys()))
ticker = CATEGORY_TICKERS[category][option]

# データ取得
data = fetch_price_history(ticker)
if data.empty:
    st.warning("データが取得できませんでした。")
else:
    metrics = compute_returns(data)

    st.subheader(f"{option}（{ticker}）のパフォーマンス")
    st.write(f"最新価格: {metrics['latest']:.2f}")
    st.metric("前日比", f"{metrics['change_from_prev_day'] * 100:.2f}%")
    st.metric("前月末比", f"{metrics['change_from_month_end'] * 100:.2f}%")
    st.metric("前年末比", f"{metrics['change_from_year_end'] * 100:.2f}%")

    # オプション：折れ線グラフ
    st.line_chart(data)
