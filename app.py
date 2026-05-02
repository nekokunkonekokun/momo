import streamlit as st
import yfinance as yf
import feedparser
import urllib.parse
import pandas as pd

# ページ設定
st.set_page_config(page_title="いっちょう Dashboard", layout="centered")

# --- データ取得関数（キャッシュを利用して軽量化） ---
@st.cache_data(ttl=3600)
def get_news(query, count=5):
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    feed = feedparser.parse(url)
    return [{"title": e.title, "link": e.link, "date": e.published} for e in feed.entries[:count]]

@st.cache_data(ttl=600)
def get_stock_price(ticker_code):
    ticker = yf.Ticker(ticker_code)
    # 2026年現在の仕様に合わせfast_infoを使用
    return ticker.fast_info['last_price']

# --- メイン画面構成 ---

# 1. ヘッダー
st.title("いっちょう Dashboard")
st.caption("親会社：クリエイト・レストランツ・ホールディングス (3387.T)")

# 2. 市場情報（最上部へ移動）
st.divider()
col1, col2 = st.columns([1, 1])

with col1:
    try:
        price = get_stock_price("3387.T")
        st.metric(label="親会社 最新株価", value=f"{price:,.1f} JPY")
    except:
        st.error("株価取得エラー")

with col2:
    st.write("詳細な分析・推移")
    st.link_button("チャートを別パネルで開く ↗", "https://finance.yahoo.co.jp/quote/3387.T/chart")

# 3. ニュースセクション
st.divider()
st.subheader("最新トピックス (自動取得)")
news_items = get_news("クリエイト・レストランツ・ホールディングス OR いっちょう 飲食店")

if news_items:
    for item in news_items:
        st.markdown(f"**[{item['title']}]({item['link']})**")
        st.caption(f"公開日: {item['date']}")
        st.write("") # スペース用
else:
    st.write("現在、新しいニュースはありません。")

# 4. フッター
st.divider()
