import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from services import (
    get_leaderboard_data,
    fetch_stock_data,
    fetch_news,
    analyze_sentiment,
    highlight_keywords,
    DEFAULT_TICKERS
)

# Streamlit App Configuration
st.set_page_config(
    page_title="Stock Analyst Dashboard",
    page_icon="📈",
    layout="wide"
)

# --- Sidebar ---
with st.sidebar:
    st.title("Settings")
    
    # Refresh button
    if st.button("Refresh Data", type="primary", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
        
    st.divider()
    
    # Filter stocks
    search_query = st.text_input("Filter Stock (Ticker)", placeholder="e.g., AAPL").upper()
    
    # Timeframe selection
    chart_period = st.selectbox("Chart Timeframe", ["1mo", "3mo", "6mo", "1y", "2y"], index=2)
    sma_window = st.slider("SMA Window (Days)", min_value=10, max_value=100, value=20, step=10)

# --- Main Dashboard ---
st.title("📊 Stock Analyst Dashboard")
st.markdown("Live financial news sentiment analysis and price tracking.")

# Get Leaderboard Data
with st.spinner("Fetching market data and sentiment..."):
    tickers_to_fetch = [search_query] if search_query else DEFAULT_TICKERS
    try:
        leaderboard_df = get_leaderboard_data(tickers_to_fetch)
    except Exception as e:
        st.error(f"Error loading leaderboard: {e}")
        leaderboard_df = pd.DataFrame()

if not leaderboard_df.empty:
    st.subheader("🏆 Sentiment Leaderboard")
    
    # Function to apply color styling to pandas dataframe
    def color_sentiment(val):
        color = 'gray'
        if val == 'Positive':
            color = 'green'
        elif val == 'Negative':
            color = 'red'
        return f'color: {color}; font-weight: bold'

    styled_df = leaderboard_df.style.applymap(color_sentiment, subset=['Sentiment Category'])
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )
    
    # CSV Export
    csv = leaderboard_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Leaderboard CSV",
        data=csv,
        file_name='sentiment_leaderboard.csv',
        mime='text/csv',
    )
    
    st.divider()
    
    # Select a stock for detailed view
    st.subheader("🔍 Stock Detailed Analysis")
    selected_ticker = st.selectbox("Select a stock for deeper analysis:", leaderboard_df['Ticker'].tolist())
    
    if selected_ticker:
        st.markdown(f"### {selected_ticker} Analysis")
        
        # Fetch detailed data for selected ticker
        with st.spinner(f"Loading {selected_ticker} data..."):
            hist_data = fetch_stock_data([selected_ticker], period=chart_period)
            news_data = fetch_news(selected_ticker)
            score, category, analyzed_news = analyze_sentiment(news_data)
            
            # Extract single ticker data
            if isinstance(hist_data, dict): # Mock data
                df = hist_data[selected_ticker]
            else:
                if selected_ticker in hist_data.columns.levels[0]:
                    df = hist_data[selected_ticker].dropna()
                else:
                    df = hist_data.dropna()
                    
            # Calculate SMA
            df[f'SMA_{sma_window}'] = df['Close'].rolling(window=sma_window).mean()
            
            # Get latest values for metrics
            current_price = df['Close'].iloc[-1]
            prev_price = df['Close'].iloc[-2] if len(df) > 1 else current_price
            price_change = ((current_price - prev_price) / prev_price) * 100
            
            current_sma = df[f'SMA_{sma_window}'].iloc[-1]
            sma_diff = ((current_price - current_sma) / current_sma) * 100 if not pd.isna(current_sma) else 0

        # --- Metrics Row ---
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current Price", f"${current_price:.2f}", f"{price_change:.2f}%")
        col2.metric(f"SMA ({sma_window})", f"${current_sma:.2f}" if not pd.isna(current_sma) else "N/A", f"{sma_diff:.2f}% vs Price")
        col3.metric("Sentiment Score", score)
        col4.metric("Recommendation", "BUY" if score > 1 else ("SELL" if score < -1 else "HOLD"))

        # --- Chart ---
        fig = go.Figure()
        
        # Price Area
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Close'],
            fill='tozeroy',
            mode='lines',
            line=dict(color='#F63366', width=2),
            name='Close Price'
        ))
        
        # SMA Line
        fig.add_trace(go.Scatter(
            x=df.index, y=df[f'SMA_{sma_window}'],
            mode='lines',
            line=dict(color='#00FFFF', width=2, dash='dash'),
            name=f'{sma_window}-Day SMA'
        ))
        
        fig.update_layout(
            title=f"{selected_ticker} Price & {sma_window}-Day SMA",
            xaxis_title="Date",
            yaxis_title="Price ($)",
            template="plotly_dark",
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # --- News Panel ---
        st.subheader("📰 Recent News & Sentiment Drivers")
        for article in analyzed_news:
            with st.container():
                st.markdown(f"#### [{article.get('title', 'No Title')}]({article.get('link', '#')})")
                
                # Render summary with highlighted keywords
                summary = article.get('summary', 'No summary available.')
                highlighted_summary = highlight_keywords(summary)
                st.markdown(f"> {highlighted_summary}", unsafe_allow_html=True)
                
                # Show article specific sentiment
                art_score = article.get('sentiment_score', 0)
                art_cat = article.get('sentiment_category', 'Neutral')
                color = "green" if art_score > 0 else ("red" if art_score < 0 else "gray")
                st.markdown(f"**Score:** <span style='color:{color}'>{art_score} ({art_cat})</span>", unsafe_allow_html=True)
                st.divider()

else:
    st.info("No data available to display.")
