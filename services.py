import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import random
from datetime import datetime, timedelta

POSITIVE_KEYWORDS = ["good", "great", "excellent", "fantastic", "bullish", "growth", "profit", "record", "surge", "upgrade"]
NEGATIVE_KEYWORDS = ["bad", "poor", "terrible", "worst", "bearish", "loss", "decline", "drop", "slump", "downgrade"]

# Top 20 stocks for mock/default
DEFAULT_TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "BRK-B", "TSM",
    "UNH", "V", "JNJ", "WMT", "JPM", "PG", "MA", "HD", "CVX", "LLY", "ABBV"
]

@st.cache_data(ttl=3600)
def fetch_stock_data(tickers, period="6mo"):
    """Fetch historical stock data for multiple tickers."""
    try:
        data = yf.download(tickers, period=period, group_by='ticker', threads=True)
        return data
    except Exception as e:
        st.warning(f"Error fetching real data: {e}. Falling back to mock data.")
        return generate_mock_stock_data(tickers)

@st.cache_data(ttl=3600)
def fetch_news(ticker):
    """Fetch news for a specific ticker."""
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        return news
    except Exception as e:
        return generate_mock_news(ticker)

def generate_mock_stock_data(tickers, days=180):
    """Generate mock historical price data."""
    dates = [datetime.now() - timedelta(days=i) for i in range(days)]
    dates.reverse()
    
    mock_data = {}
    for ticker in tickers:
        base_price = random.uniform(50, 500)
        prices = [base_price]
        for _ in range(days - 1):
            change = prices[-1] * random.uniform(-0.03, 0.03)
            prices.append(prices[-1] + change)
        
        df = pd.DataFrame({
            'Close': prices
        }, index=dates)
        mock_data[ticker] = df
        
    return mock_data

def generate_mock_news(ticker):
    """Generate mock news articles containing trigger keywords."""
    num_articles = random.randint(3, 8)
    news = []
    
    for i in range(num_articles):
        pos_word = random.choice(POSITIVE_KEYWORDS)
        neg_word = random.choice(NEGATIVE_KEYWORDS)
        words = [pos_word, neg_word, "market", "investors", "report", "earnings"]
        random.shuffle(words)
        
        title = f"{ticker} sees {words[0]} performance amid {words[1]} outlook."
        summary = f"The company reported {words[2]} results that were {words[3]}. Experts say this is a {words[4]} sign."
        
        news.append({
            'title': title,
            'summary': summary,
            'link': '#',
            'providerPublishTime': int((datetime.now() - timedelta(hours=random.randint(1, 48))).timestamp())
        })
    return news

def analyze_sentiment(news_list):
    """Analyze sentiment of a list of news articles based on keywords."""
    score = 0
    analyzed_articles = []
    
    for article in news_list:
        text_to_scan = f"{article.get('title', '')} {article.get('summary', '')}".lower()
        
        pos_count = sum(text_to_scan.count(word) for word in POSITIVE_KEYWORDS)
        neg_count = sum(text_to_scan.count(word) for word in NEGATIVE_KEYWORDS)
        
        article_score = pos_count - neg_count
        score += article_score
        
        # Add sentiment info to article
        article['sentiment_score'] = article_score
        if article_score > 0:
            article['sentiment_category'] = 'Positive'
        elif article_score < 0:
            article['sentiment_category'] = 'Negative'
        else:
            article['sentiment_category'] = 'Neutral'
            
        analyzed_articles.append(article)
        
    category = "Neutral"
    if score > 0:
        category = "Positive"
    elif score < 0:
        category = "Negative"
        
    return score, category, analyzed_articles

def highlight_keywords(text):
    """Wrap keywords in HTML for highlighting in Streamlit."""
    text_lower = text.lower()
    highlighted_text = text
    
    # Highlight positive keywords in green
    for word in POSITIVE_KEYWORDS:
        if word in text_lower:
            # Case insensitive replace is trickier, simplified for this example
            import re
            pattern = re.compile(f"\\b{word}\\b", re.IGNORECASE)
            highlighted_text = pattern.sub(f'<span style="color: #00FF00; font-weight: bold;">{word}</span>', highlighted_text)
            
    # Highlight negative keywords in red
    for word in NEGATIVE_KEYWORDS:
        if word in text_lower:
            import re
            pattern = re.compile(f"\\b{word}\\b", re.IGNORECASE)
            highlighted_text = pattern.sub(f'<span style="color: #FF0000; font-weight: bold;">{word}</span>', highlighted_text)
            
    return highlighted_text

@st.cache_data(ttl=3600)
def get_leaderboard_data(tickers=DEFAULT_TICKERS):
    """Generate leaderboard data by analyzing sentiment and fetching current prices."""
    leaderboard = []
    
    # Fetch historical data to get the current price
    hist_data = fetch_stock_data(tickers, period="5d")
    
    for ticker in tickers:
        news = fetch_news(ticker)
        score, category, _ = analyze_sentiment(news)
        
        current_price = 0.0
        try:
            if isinstance(hist_data, dict): # mock data
                current_price = hist_data[ticker]['Close'].iloc[-1]
            elif ticker in hist_data.columns.levels[0]: # MultiIndex from yf.download group_by='ticker'
                current_price = hist_data[ticker]['Close'].dropna().iloc[-1]
            else:
                # Single ticker fallback if only 1 ticker was passed, which doesn't use MultiIndex in the same way
                current_price = hist_data['Close'].dropna().iloc[-1]
        except Exception as e:
            current_price = random.uniform(50, 500) # fallback
            
        leaderboard.append({
            'Ticker': ticker,
            'Company Name': ticker, # Simplifying, yfinance info for name is slow
            'Sentiment Score': score,
            'Sentiment Category': category,
            'Current Price': round(current_price, 2)
        })
        
    # Sort by sentiment score descending
    leaderboard.sort(key=lambda x: x['Sentiment Score'], reverse=True)
    return pd.DataFrame(leaderboard)
