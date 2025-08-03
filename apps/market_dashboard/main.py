import streamlit as st
import pandas as pd
import sys, os
from datetime import datetime, timedelta

# プロジェクトルートを sys.path に追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from apps.market_dashboard.data_fetcher import fetch_price_history
from apps.market_dashboard.metrics import compute_returns_custom
from apps.market_dashboard.config import CATEGORY_TICKERS

st.set_page_config(page_title="Market Dashboard", layout="wide")
st.title("📈 市況モニターダッシュボード")

# 📅 日付選択
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("開始日", datetime.today() - timedelta(days=180))
with col2:
    end_date = st.date_input("終了日", datetime.today())

if start_date >= end_date:
    st.error("開始日は終了日より前である必要があります。")
    st.stop()

# 📂 カテゴリ・タグ・銘柄選択
category = st.selectbox("カテゴリを選択", CATEGORY_TICKERS.keys())
tags = CATEGORY_TICKERS[category]
tag = st.selectbox("タグを選択", tags.keys())
tickers = tags[tag]

st.markdown("### 表示する銘柄を選択")
selected_labels = [
    label for label in tickers if st.checkbox(label, value=True)
]



# 📊 表データ構築
summary_data = []

for label in selected_labels:
    ticker = tickers[label]
    data = fetch_price_history(ticker, start=str(start_date), end=None)  # ← end=Noneで最新まで取得
    if data.empty:
        continue
    metrics = compute_returns_custom(data, start_date, end_date)
    def format_pct(value):
        return f"{value * 100:.2f}%" if value is not None else ""

    
    summary_data.append({
        "銘柄": label,
        "タグ": tag,
        "カテゴリ": category,
        "開始値": metrics["start"],
        "終了値": metrics["end"],
        "直近値": metrics["latest"],
        "乖離": format_pct(metrics["deviation"]),
        "DTD": format_pct(metrics["change_from_prev_day"]),
        "MTD": format_pct(metrics["change_from_month_end"]),
        "YTD": format_pct(metrics["change_from_year_end"]),
    })

if summary_data:
    st.subheader("📊 サマリー表")
    df = pd.DataFrame(summary_data)
    st.dataframe(df)
else:
    st.warning("表示対象の銘柄がありません。")

# 📈 チャート表示
if len(selected_labels) == 1:
    label = selected_labels[0]
    ticker = tickers[label]
    st.subheader(f"📈 {label} の価格推移")
    chart_data = fetch_price_history(ticker, start=str(start_date), end=None)
    if not chart_data.empty:
        st.line_chart(chart_data)
    else:
        st.warning("チャートデータが取得できませんでした。")
