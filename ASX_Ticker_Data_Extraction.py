import streamlit as st
import yfinance as yf
import pandas as pd
import io

# -----------------------------
st.set_page_config(page_title="Stock Data Downloader", layout="wide", page_icon="📈")
st.title("📈 Stock Data Downloader — Closing Price (Full History)")

# -----------------------------
user_ticker = st.text_input("Enter a single ticker (without exchange suffix):")

if user_ticker:
    ticker = user_ticker.strip().upper()
    # If always ASX: uncomment next line
    # ticker = ticker + ".AX"

    with st.spinner(f"Fetching data for {ticker}, please wait..."):
        try:
            data = yf.download(ticker, period="1000d", progress=False)
            
            if data.empty or 'Close' not in data.columns:
                st.error(f"No valid data returned for {ticker}. Please check the ticker symbol.")
            else:
                df = data.reset_index()[['Date', 'Close']]
                df['Ticker'] = ticker

                # Download button (no table displayed)
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_buffer.getvalue(),
                    file_name=f"{ticker}_data.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"Failed to fetch data for {ticker}: {e}")

