# Specification: Python-Based Stock Analyst Dashboard

Build a modern, highly interactive **Stock Analyst Dashboard** using **only Python**. The application must ingest financial news, perform keyword-based sentiment analysis, rank and display top performing/underperforming stocks, and visualize price/chart data with technical indicators.

---

## 🛠️ Technology Stack
- **Framework:** Streamlit (for building interactive web apps entirely in Python)
- **Data Manipulation:** `pandas`, `numpy`
- **Visualization:** `plotly` (or native Streamlit interactive charts) for price history and moving averages
- **APIs & Feeds:** `yfinance` (Yahoo Finance library for Python) and standard RSS fetching (`requests`, `xml.etree.ElementTree`)
- **Styling:** Streamlit native layout, custom theme configurations (sleek dark mode default), and markdown/HTML injections for key highlights

---

## 🔌 API & Data Strategy (Free Sources & Python Safety)
Ensure the application runs seamlessly out-of-the-box by implementing a robust data ingestion layer:

1. **Live Data Collection:**
   - Fetch ticker-specific news and historical prices directly using the free `yfinance` library.
   - Fall back to standard RSS parsing of Yahoo Finance news feeds if specific ticker endpoints rate-limit.
2. **Local Mock Data & Simulation:**
   - Include a pre-defined set of 20+ major stock tickers (e.g., AAPL, MSFT, GOOGL, AMZN, TSLA, etc.).
   - If no network connection is available or API limits are hit, automatically generate realistic synthetic price trends and mock news articles containing trigger keywords.
3. **Caching:**
   - Use Streamlit's caching mechanisms (`@st.cache_data` or `@st.cache_resource`) to speed up loading and prevent redundant API hits on user interactions.

---

## ⚙️ Core Sentiment Engine (Python)
1. **Keyword Analyzer:**
   - Implement a simple Python function to scan news titles and summaries for:
     - **Positive Keywords (+1 score each):** `good`, `great`, `excellent`, `fantastic`, `bullish`, `growth`, `profit`, `record`, `surge`, `upgrade`
     - **Negative Keywords (-1 score each):** `bad`, `poor`, `terrible`, `worst`, `bearish`, `loss`, `decline`, `drop`, `slump`, `downgrade`
2. **Sentiment Scoring:** Compute a compound score for each stock based on all keywords found across its linked news articles.
3. **Ranking:** Sort and showcase the top 20 stocks by their compound sentiment score.

---

## 🖥️ UI & Feature Requirements (Streamlit Design)

### 1. Dashboard Layout
- **Sidebar:** Navigation, search input to filter specific stocks, refresh button, and configuration settings (e.g., selection of chart timeframes).
- **Main Viewport:** Split into a Leaderboard panel (top) and Detail views (bottom/columns) once a stock is selected.
- Configured with a default dark theme (`.streamlit/config.toml` styled with a dark background, vibrant accent colors, and custom fonts).

### 2. Stock Leaderboard List
- Interactive table showing the top 20 stocks.
- Columns: Ticker, Company Name, Sentiment Score, Sentiment Category (Positive/Negative/Neutral), and Current Price.
- Apply conditional formatting (e.g., cell coloring or emoji badges) based on sentiment category.

### 3. Interactive Charts
- On selecting a stock from the list:
  - Display an interactive line/area chart of the stock's closing price (e.g., last 30-180 days).
  - Compute and plot a **Simple Moving Average (SMA)** (e.g., 20-day or 50-day) overlaid on the price chart using Pandas rolling window calculations.
- Display key metrics side-by-side: Current Price, SMA Price, Percentage difference, and Sentiment Score.

### 4. News & Sentiment Analysis Panel
- Display a clean list of news articles associated with the selected stock.
- Highlight the matched positive/negative keywords directly in the UI text (using basic HTML/CSS injections inside Streamlit's `st.write` or `st.markdown`).
- Provide an analysis breakdown summary box showing recommendations (e.g., BUY, SELL, or HOLD) based on score thresholds.

### 5. Control Actions
- **Refresh Data:** A prominent button that clears the Streamlit cache and triggers a fresh fetch/re-run.
- **CSV Export:** Use Streamlit's native `st.download_button` to immediately download the current 20-stock leaderboard as a CSV file.

---

## 🚀 Step-by-Step Implementation Path

1. **Environment Setup:**
   - Create a Python virtual environment and set up `requirements.txt` (`streamlit`, `pandas`, `plotly`, `yfinance`, `requests`).
   - Create Streamlit configuration in `.streamlit/config.toml` to enforce a dark theme.
2. **Data & Sentiment Service (`services.py`):**
   - Write functions to fetch stock metadata, historical prices, and news feed data.
   - Write the keyword sentiment parser.
   - Implement the mock database fallback.
3. **App Architecture (`app.py`):**
   - Build the sidebar structure (search, refresh, parameters).
   - Implement data caching logic.
   - Render the leaderboard table with conditional styling.
4. **Detail Visualization:**
   - Draw interactive Plotly charts with price line + SMA overlay.
   - Render keyword-highlighted news articles and analysis metrics.
5. **Testing & Verification:**
   - Verify cache behavior during refresh actions.
   - Verify CSV export formatting.
