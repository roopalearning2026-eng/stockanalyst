# Stock Analyst Dashboard

A modern, highly interactive Python-based dashboard for financial analysis. Built with **Streamlit**, this application provides live financial data tracking, interactive price charts, and an automated keyword-based sentiment engine to gauge the market mood on various stocks.

## 🚀 Features

- **Sentiment Leaderboard**: Ranks top stocks (like AAPL, MSFT, TSLA, etc.) based on real-time news sentiment.
- **Automated Sentiment Engine**: Scans recent news articles for positive/negative triggers and assigns an aggregate score.
- **Interactive Price Charts**: Utilizes `plotly` to render beautiful price history charts with dynamically calculated Simple Moving Averages (SMA) overlaid.
- **Keyword Highlights**: The news panel automatically highlights trigger keywords (e.g., green for 'growth', red for 'loss') directly in the UI.
- **Robust Data Fallbacks**: Powered by the free `yfinance` library. If rate-limits are hit or offline, the app seamlessly falls back to a locally generated mock dataset.
- **CSV Export**: Instantly download the sentiment leaderboard to a CSV file.
- **Sleek Dark Mode UI**: Customized through `.streamlit/config.toml` for a premium viewing experience.

## 🛠️ Technology Stack

- **Framework**: [Streamlit](https://streamlit.io/)
- **Data Manipulation**: `pandas`, `numpy`
- **Visualization**: `plotly`
- **APIs & Data**: `yfinance`, `requests`

## ⚙️ Setup and Installation

### 1. Prerequisites
Ensure you have Python 3.9+ installed on your system.

### 2. Clone the Repository
```bash
git clone <your-repo-url>
cd StockAnalyst
```

### 3. Setup Virtual Environment
It is recommended to run this project in an isolated virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Variables
A `.env` template file has been provided. The application currently functions out-of-the-box utilizing free Yahoo Finance data via `yfinance`. If you choose to integrate premium data sources later, you can add your API keys to the `.env` file.

### 6. Run the Application
Start the Streamlit development server:

```bash
streamlit run app.py
```
This will automatically open the dashboard in your default web browser at `http://localhost:8501`.

## 📁 Project Structure

- `app.py`: The main Streamlit frontend application, defining layout and interactions.
- `services.py`: The backend layer containing API fetchers, the sentiment engine, caching logic, and mock data generators.
- `.streamlit/config.toml`: UI configuration enforcing the custom dark theme.
- `requirements.txt`: Python package dependencies.
- `.env`: Template file for any necessary API keys.

## 📝 License
This project is open-source and available under the MIT License.
