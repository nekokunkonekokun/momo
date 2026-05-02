import streamlit as st
import yfinance as yf
import feedparser
import urllib.parse
import pandas as pd

# ページ設定
st.set_page_config(page_title="いっちょう Dashboard", layout="centered")

# --- データ取得関数（キャッシュを利用して軽量化） ---
@st.cache_data(ttl=3600)  # 1時間キャッシュ
def get_news(query, count=5):
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    feed = feedparser.parse(url)
    return [{"title": e.title, "link": e.link, "date": e.published} for e in feed.entries[:count]]

@st.cache_data(ttl=600)  # 10分キャッシュ
def get_stock_price(ticker_code):
    ticker = yf.Ticker(ticker_code)
    return ticker.fast_info['last_price']

# --- メイン画面 ---
st.title("いっちょう Dashboard")
st.caption("親会社：クリエイト・レストランツ・ホールディングス (3387.T) 分析")

# ニュースセクション
st.subheader("最新トピックス")
news_items = get_news("クリエイト・レストランツ・ホールディングス OR いっちょう 飲食店")

for item in news_items:
    st.markdown(f"**[{item['title']}]({item['link']})**")
    st.caption(f"公開日: {item['date']}")
    st.divider()

# 株価パネル
st.subheader("市場情報")
col1, col2 = st.columns([1, 1])

with col1:
    price = get_stock_price("3387.T")
    st.metric(label="親会社 最新株価", value=f"{price:,.1f} JPY")

with col2:
    st.write("詳細な分析はこちら")
    st.link_button("チャートを別パネルで開く ↗", "https://finance.yahoo.co.jp/quote/3387.T/chart")

# 注意事項
st.info("※ハルシネーション（AIの嘘）を疑え。公式IR情報を必ず確認してください。")

