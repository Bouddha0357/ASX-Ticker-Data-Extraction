import streamlit as st
import yfinance as yf
import pandas as pd
import io

# -----------------------------
# Config
st.set_page_config(page_title="Stock Data Downloader", layout="wide", page_icon="📈")
st.title("📈 Stock Data Downloader — Closing Price (Full History)")

# -----------------------------
# User input for ticker
user_ticker = st.text_input("Enter a single ticker (without exchange suffix):")

if user_ticker:
    # Format ticker (e.g. uppercase)
    ticker = user_ticker.strip().upper()
    # If needed, append exchange suffix (e.g. `.AX`)
    # ticker = ticker + ".AX"

    with st.spinner(f"Fetching data for {ticker}, please wait..."):
        try:
            # Use period="max" to get the entire available history
            data = yf.download(ticker, period="max", progress=False)
            
            if data.empty or 'Close' not in data.columns:
                st.error(f"No valid data returned for {ticker}. Please check the ticker symbol.")
            else:
                # Prepare DataFrame with Date and Close
                df = data.reset_index()[['Date', 'Close']]
                df['Ticker'] = ticker

                # Show preview (last 10 rows)
                st.dataframe(df.tail(10))

                # Download button
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



