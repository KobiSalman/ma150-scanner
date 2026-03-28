import streamlit as st
import yfinance as yf
import pandas as pd


st.set_page_config(page_title="MA150 Scanner", layout="wide")


@st.cache_data(ttl=3600)
def load_symbols(csv_path: str = "symbols.csv") -> list[str]:
    symbols_df = pd.read_csv(csv_path)
    symbols = (
        symbols_df["Symbol"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )
    return symbols


def scan_stocks(symbols: list[str]) -> pd.DataFrame:
    results = []

    progress_bar = st.progress(0)
    status_text = st.empty()

    total = len(symbols)

    for index, symbol in enumerate(symbols, start=1):
        try:
            status_text.text(f"Scanning {symbol} ({index}/{total})...")

            data = yf.download(
                symbol,
                period="200d",
                progress=False,
                multi_level_index=False,
                auto_adjust=False,
            )

            if data.empty or len(data) < 150:
                progress_bar.progress(index / total)
                continue

            if "Close" not in data.columns:
                progress_bar.progress(index / total)
                continue

            data["MA150"] = data["Close"].rolling(150).mean()
            data = data.dropna()

            if data.empty:
                progress_bar.progress(index / total)
                continue

            latest = data.iloc[-1]

            close = float(latest["Close"])
            ma150 = float(latest["MA150"])

            if close > ma150:
                diff_pct = ((close - ma150) / ma150) * 100

                results.append(
                    {
                        "Symbol": symbol,
                        "Close": round(close, 2),
                        "MA150": round(ma150, 2),
                        "% Above MA150": round(diff_pct, 2),
                    }
                )

        except Exception:
            pass

        progress_bar.progress(index / total)

    status_text.text("Scan complete.")

    df = pd.DataFrame(results)

    if not df.empty:
        df = df.sort_values(by="% Above MA150", ascending=False).reset_index(drop=True)

    return df


st.title("Stocks Above MA150")
st.write("המערכת מציגה רק מניות שנסחרות מעל ממוצע נע 150.")

try:
    symbols = load_symbols("symbols.csv")
    st.success(f"Loaded {len(symbols)} symbols from symbols.csv")
except Exception as e:
    st.error(f"Failed to load symbols.csv: {e}")
    st.stop()

run_scan = st.button("Run Scan")

if run_scan:
    with st.spinner("Scanning stocks..."):
        results_df = scan_stocks(symbols)

    st.subheader("Results")

    if results_df.empty:
        st.warning("No stocks above MA150.")
    else:
        st.write(f"Found {len(results_df)} stocks above MA150.")
        st.dataframe(results_df, use_container_width=True)

        csv_data = results_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="Download results as CSV",
            data=csv_data,
            file_name="ma150_results.csv",
            mime="text/csv",
        )