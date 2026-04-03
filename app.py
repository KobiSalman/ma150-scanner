import streamlit as st
import yfinance as yf
import pandas as pd


st.set_page_config(
    page_title="SimpliTrade Radar",
    page_icon="📈",
    layout="wide",
)


st.markdown(
    """
    <style>
    .stApp {
        background-color: #f8fafc;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    .topbar {
        display: flex;
        justify-content: flex-start;
        align-items: center;
        margin-bottom: 1.2rem;
    }

    .app-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.3rem;
    }

    .app-subtitle {
        font-size: 1rem;
        color: #475569;
        margin-bottom: 1.8rem;
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 0.8rem;
    }

    .small-text {
        color: #64748b;
        font-size: 0.95rem;
        margin-bottom: 1rem;
    }

    .status-box-good {
        background: #ecfdf5;
        border: 1px solid #10b981;
        color: #065f46;
        padding: 16px;
        border-radius: 14px;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 1rem;
    }

    .status-box-bad {
        background: #fef2f2;
        border: 1px solid #ef4444;
        color: #991b1b;
        padding: 16px;
        border-radius: 14px;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 1rem;
    }

    .analysis-box {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 18px;
        margin-top: 1rem;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
        color: #0f172a;
        line-height: 1.8;
        white-space: pre-line;
    }

    .analysis-box-he {
        direction: rtl;
        text-align: right;
    }

    .analysis-box-en {
        direction: ltr;
        text-align: left;
    }

    .scale-wrapper {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .scale-label {
        font-size: 0.95rem;
        font-weight: 600;
        color: #334155;
        margin-bottom: 0.45rem;
    }

    .scale-bar {
        position: relative;
        width: 100%;
        height: 18px;
        border-radius: 999px;
        background: linear-gradient(90deg, #dc2626 0%, #f97316 25%, #facc15 50%, #84cc16 75%, #16a34a 100%);
        box-shadow: inset 0 0 0 1px rgba(15, 23, 42, 0.08);
    }

    .scale-marker {
        position: absolute;
        top: 50%;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: #0f172a;
        border: 3px solid white;
        transform: translate(-50%, -50%);
        box-shadow: 0 2px 8px rgba(0,0,0,0.18);
    }

    .scale-footer {
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        color: #64748b;
        margin-top: 0.35rem;
    }

    .bias-pill {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        font-size: 0.92rem;
        font-weight: 700;
        margin-top: 0.75rem;
        margin-bottom: 0.25rem;
    }

    .bias-bullish {
        background: #dcfce7;
        color: #166534;
        border: 1px solid #86efac;
    }

    .bias-watch {
        background: #ecfccb;
        color: #4d7c0f;
        border: 1px solid #bef264;
    }

    .bias-neutral {
        background: #fef9c3;
        color: #854d0e;
        border: 1px solid #fde68a;
    }

    .bias-bearish {
        background: #fee2e2;
        color: #991b1b;
        border: 1px solid #fca5a5;
    }

    div.stButton > button {
        border-radius: 12px;
        height: 44px;
        font-weight: 600;
        border: none;
        background: #2563eb;
        color: white;
    }

    div.stDownloadButton > button {
        border-radius: 12px;
        height: 44px;
        font-weight: 600;
    }

    div[data-baseweb="input"] > div {
        border-radius: 12px;
        border: 1px solid #cbd5e1;
        background: white;
    }

    /* language segmented control */
    div[data-testid="stSegmentedControl"] {
        max-width: 220px;
    }

    div[data-testid="stSegmentedControl"] button {
        min-width: 90px;
        font-weight: 600;
        border-radius: 10px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


TEXT = {
    "en": {
        "app_title": "📈 SimpliTrade Radar",
        "app_subtitle": "A clean and simple tool to scan stocks above the 150-day moving average and explain technical conditions in plain English.",
        "scanner_tab": "Scanner",
        "ticker_tab": "Single Ticker",
        "stock_scanner": "Stock Scanner",
        "scanner_desc": "Displays stocks trading above the 150-day moving average.",
        "total_symbols": "Total Symbols",
        "scan_type": "Scan Type",
        "mode": "Mode",
        "above_only": "Above Only",
        "run_scan": "Run Scan",
        "scanning_stocks": "Scanning stocks...",
        "scan_complete": "Scan complete.",
        "no_stocks_found": "No stocks found above MA150.",
        "stocks_found": "Found {count} stocks above MA150.",
        "sorted_caption": "Sorted by strength above MA150 (highest first)",
        "download_csv": "Download CSV",
        "single_ticker_title": "Single Ticker Analysis",
        "single_ticker_desc": "Enter a ticker and get a plain-English technical explanation without reading the chart yourself.",
        "ticker_placeholder": "Example: AAPL",
        "analyze_stock": "Analyze Stock",
        "invalid_ticker": "Please enter a valid ticker (no spaces).",
        "unable_fetch": "Unable to fetch data for this ticker or not enough historical data.",
        "checking": "Checking {ticker}...",
        "ticker": "Ticker",
        "close": "Close",
        "ma150": "MA150",
        "distance": "Distance",
        "above_ma150": "✅ {symbol} is ABOVE MA150",
        "below_ma150": "❌ {symbol} is BELOW MA150",
        "scale_label": "Overall Technical Position",
        "bearish": "Bearish",
        "neutral": "Neutral",
        "bullish": "Bullish",
        "bias_bullish": "BULLISH",
        "bias_watch": "WATCH",
        "bias_neutral": "NEUTRAL",
        "bias_bearish": "BEARISH",
        "technical_score": "Score",
        "failed_symbols": "Failed to load symbols.csv: {error}",
        "supportive_signals": "Supportive signals:",
        "limiting_factors": "Limiting factors:",
        "technical_summary": "{symbol} Technical Summary",
        "conclusion_title": "Conclusion:",
        "distance_above": "The stock is trading {diff}% above MA150, which supports the long-term trend.",
        "distance_below": "The stock is trading {diff}% below MA150, which weakens the long-term picture.",
        "rsi_extended": "RSI is {rsi}, which suggests momentum is strong but the stock may be somewhat extended.",
        "rsi_bullish": "RSI is {rsi}, which reflects healthy bullish momentum.",
        "rsi_neutral": "RSI is {rsi}, which reflects neutral momentum.",
        "rsi_weak": "RSI is {rsi}, which reflects weak momentum.",
        "price_above_150": "Price is above the 150-day moving average",
        "price_below_150": "Price is below the 150-day moving average",
        "price_above_50": "Price is above the 50-day moving average",
        "price_below_50": "Price is below the 50-day moving average",
        "price_above_20": "Price is above the 20-day moving average",
        "price_below_20": "Price is below the 20-day moving average",
        "ma150_rising": "The 150-day moving average is rising",
        "ma150_not_rising": "The 150-day moving average is not rising",
        "ma50_rising": "The 50-day moving average is rising",
        "ma50_not_rising": "The 50-day moving average is not rising",
        "ma20_rising": "The 20-day moving average is rising",
        "ma20_not_rising": "The 20-day moving average is not rising",
        "conclusion_bullish": "{symbol} shows strong technical alignment. Trend and momentum are supportive across multiple signals.",
        "conclusion_watch": "{symbol} shows constructive technical conditions, but not a fully confirmed setup yet. It is worth monitoring for stronger alignment.",
        "conclusion_neutral": "{symbol} shows mixed technical conditions. There are some supportive signals, but the overall structure is not fully convincing yet.",
        "conclusion_bearish": "{symbol} currently shows weak technical structure. The broader setup is not supportive right now.",
    },
    "he": {
        "app_title": "📈 SimpliTrade Radar",
        "app_subtitle": "כלי פשוט ונקי לסריקת מניות מעל ממוצע נע 150 ולהסבר מצב טכני בשפה ברורה.",
        "scanner_tab": "סורק",
        "ticker_tab": "טיקר בודד",
        "stock_scanner": "סורק מניות",
        "scanner_desc": "מציג מניות שנסחרות מעל ממוצע נע 150.",
        "total_symbols": "כמות טיקרים",
        "scan_type": "סוג סריקה",
        "mode": "מצב",
        "above_only": "מעל בלבד",
        "run_scan": "הרץ סריקה",
        "scanning_stocks": "סורק מניות...",
        "scan_complete": "הסריקה הסתיימה.",
        "no_stocks_found": "לא נמצאו מניות מעל MA150.",
        "stocks_found": "נמצאו {count} מניות מעל MA150.",
        "sorted_caption": "ממויין לפי עוצמה מעל MA150 מהגבוה לנמוך",
        "download_csv": "הורד CSV",
        "single_ticker_title": "ניתוח טיקר בודד",
        "single_ticker_desc": "הזן טיקר וקבל הסבר טכני ברור בלי צורך לקרוא את הגרף בעצמך.",
        "ticker_placeholder": "לדוגמה: AAPL",
        "analyze_stock": "נתח מניה",
        "invalid_ticker": "יש להזין טיקר תקין ללא רווחים.",
        "unable_fetch": "לא ניתן להביא נתונים עבור הטיקר הזה או שאין מספיק היסטוריה.",
        "checking": "בודק את {ticker}...",
        "ticker": "טיקר",
        "close": "מחיר",
        "ma150": "MA150",
        "distance": "פער",
        "above_ma150": "✅ {symbol} נמצאת מעל MA150",
        "below_ma150": "❌ {symbol} נמצאת מתחת ל־MA150",
        "scale_label": "מיקום טכני כללי",
        "bearish": "שלילי",
        "neutral": "ניטרלי",
        "bullish": "חיובי",
        "bias_bullish": "חיובי",
        "bias_watch": "למעקב",
        "bias_neutral": "ניטרלי",
        "bias_bearish": "שלילי",
        "technical_score": "ציון",
        "failed_symbols": "טעינת symbols.csv נכשלה: {error}",
        "supportive_signals": "סימנים תומכים:",
        "limiting_factors": "גורמים מגבילים:",
        "technical_summary": "סיכום טכני עבור {symbol}",
        "conclusion_title": "מסקנה:",
        "distance_above": "המניה נסחרת {diff}% מעל MA150, דבר שתומך במגמה ארוכת הטווח.",
        "distance_below": "המניה נסחרת {diff}% מתחת ל־MA150, דבר שמחליש את התמונה ארוכת הטווח.",
        "rsi_extended": "ה־RSI הוא {rsi}, מה שמצביע על מומנטום חזק אך ייתכן שהמניה כבר מעט מתוחה.",
        "rsi_bullish": "ה־RSI הוא {rsi}, מה שמשקף מומנטום חיובי בריא.",
        "rsi_neutral": "ה־RSI הוא {rsi}, מה שמשקף מומנטום ניטרלי.",
        "rsi_weak": "ה־RSI הוא {rsi}, מה שמשקף מומנטום חלש.",
        "price_above_150": "המחיר מעל ממוצע נע 150",
        "price_below_150": "המחיר מתחת לממוצע נע 150",
        "price_above_50": "המחיר מעל ממוצע נע 50",
        "price_below_50": "המחיר מתחת לממוצע נע 50",
        "price_above_20": "המחיר מעל ממוצע נע 20",
        "price_below_20": "המחיר מתחת לממוצע נע 20",
        "ma150_rising": "ממוצע נע 150 נמצא במגמת עלייה",
        "ma150_not_rising": "ממוצע נע 150 אינו במגמת עלייה",
        "ma50_rising": "ממוצע נע 50 נמצא במגמת עלייה",
        "ma50_not_rising": "ממוצע נע 50 אינו במגמת עלייה",
        "ma20_rising": "ממוצע נע 20 נמצא במגמת עלייה",
        "ma20_not_rising": "ממוצע נע 20 אינו במגמת עלייה",
        "conclusion_bullish": "{symbol} מציגה התאמה טכנית חזקה. גם המגמה וגם המומנטום תומכים בתמונה הכוללת.",
        "conclusion_watch": "{symbol} מציגה תנאים טכניים בונים, אך עדיין לא מדובר במבנה מאושר לחלוטין. שווה להמשיך לעקוב לחיזוק נוסף.",
        "conclusion_neutral": "{symbol} מציגה תמונה טכנית מעורבת. יש סימנים תומכים, אך המבנה הכולל עדיין לא מספיק משכנע.",
        "conclusion_bearish": "{symbol} מציגה כרגע מבנה טכני חלש. התמונה הרחבה אינה תומכת כרגע.",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    return TEXT[lang][key].format(**kwargs)


# Professional language switch
top_left, top_right = st.columns([1.3, 4.7])
with top_left:
    selected_language = st.segmented_control(
        "Language",
        options=["English", "עברית"],
        default="English",
        label_visibility="collapsed",
    )

lang = "he" if selected_language == "עברית" else "en"


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


def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def get_stock_data(symbol: str) -> dict | None:
    try:
        data = yf.download(
            symbol,
            period="250d",
            progress=False,
            multi_level_index=False,
            auto_adjust=False,
        )

        if data.empty or len(data) < 150 or "Close" not in data.columns:
            return None

        data["MA20"] = data["Close"].rolling(20).mean()
        data["MA50"] = data["Close"].rolling(50).mean()
        data["MA150"] = data["Close"].rolling(150).mean()
        data["RSI"] = calculate_rsi(data["Close"])
        data = data.dropna()

        if data.empty:
            return None

        latest = data.iloc[-1]
        prev_5 = data.iloc[-6] if len(data) >= 6 else None

        close = float(latest["Close"])
        ma20 = float(latest["MA20"])
        ma50 = float(latest["MA50"])
        ma150 = float(latest["MA150"])
        rsi = float(latest["RSI"])

        diff_pct = ((close - ma150) / ma150) * 100

        ma20_rising = False
        ma50_rising = False
        ma150_rising = False

        if prev_5 is not None:
            ma20_rising = ma20 > float(prev_5["MA20"])
            ma50_rising = ma50 > float(prev_5["MA50"])
            ma150_rising = ma150 > float(prev_5["MA150"])

        return {
            "Symbol": symbol.upper(),
            "Close": round(close, 2),
            "MA20": round(ma20, 2),
            "MA50": round(ma50, 2),
            "MA150": round(ma150, 2),
            "RSI": round(rsi, 2),
            "DifferencePct": round(diff_pct, 2),
            "AboveMA20": close > ma20,
            "AboveMA50": close > ma50,
            "AboveMA150": close > ma150,
            "MA20Rising": ma20_rising,
            "MA50Rising": ma50_rising,
            "MA150Rising": ma150_rising,
        }

    except Exception:
        return None


def evaluate_bias_and_score(result: dict) -> tuple[int, str]:
    score = 0

    if result["AboveMA150"]:
        score += 25
    if result["AboveMA50"]:
        score += 20
    if result["AboveMA20"]:
        score += 10

    if result["MA150Rising"]:
        score += 15
    if result["MA50Rising"]:
        score += 10
    if result["MA20Rising"]:
        score += 5

    rsi = result["RSI"]
    if 55 <= rsi <= 68:
        score += 15
    elif 45 <= rsi < 55:
        score += 8
    elif 68 < rsi <= 75:
        score += 8

    score = max(0, min(100, score))

    if score >= 80:
        bias = "BULLISH"
    elif score >= 60:
        bias = "WATCH"
    elif score >= 40:
        bias = "NEUTRAL"
    else:
        bias = "BEARISH"

    return score, bias


def local_bias(lang: str, bias: str) -> str:
    mapping = {
        "BULLISH": t(lang, "bias_bullish"),
        "WATCH": t(lang, "bias_watch"),
        "NEUTRAL": t(lang, "bias_neutral"),
        "BEARISH": t(lang, "bias_bearish"),
    }
    return mapping[bias]


def generate_analysis(result: dict, lang: str) -> tuple[str, int, str]:
    symbol = result["Symbol"]
    diff = result["DifferencePct"]
    abs_diff = abs(diff)

    supportive_signals = []
    limiting_factors = []

    if result["AboveMA150"]:
        supportive_signals.append(t(lang, "price_above_150"))
    else:
        limiting_factors.append(t(lang, "price_below_150"))

    if result["AboveMA50"]:
        supportive_signals.append(t(lang, "price_above_50"))
    else:
        limiting_factors.append(t(lang, "price_below_50"))

    if result["AboveMA20"]:
        supportive_signals.append(t(lang, "price_above_20"))
    else:
        limiting_factors.append(t(lang, "price_below_20"))

    if result["MA150Rising"]:
        supportive_signals.append(t(lang, "ma150_rising"))
    else:
        limiting_factors.append(t(lang, "ma150_not_rising"))

    if result["MA50Rising"]:
        supportive_signals.append(t(lang, "ma50_rising"))
    else:
        limiting_factors.append(t(lang, "ma50_not_rising"))

    if result["MA20Rising"]:
        supportive_signals.append(t(lang, "ma20_rising"))
    else:
        limiting_factors.append(t(lang, "ma20_not_rising"))

    rsi = result["RSI"]

    if rsi >= 70:
        rsi_text = t(lang, "rsi_extended", rsi=rsi)
    elif rsi >= 55:
        rsi_text = t(lang, "rsi_bullish", rsi=rsi)
    elif rsi >= 45:
        rsi_text = t(lang, "rsi_neutral", rsi=rsi)
    else:
        rsi_text = t(lang, "rsi_weak", rsi=rsi)

    score, bias = evaluate_bias_and_score(result)

    if result["AboveMA150"]:
        distance_text = t(lang, "distance_above", diff=diff)
    else:
        distance_text = t(lang, "distance_below", diff=abs_diff)

    if bias == "BULLISH":
        conclusion = t(lang, "conclusion_bullish", symbol=symbol)
    elif bias == "WATCH":
        conclusion = t(lang, "conclusion_watch", symbol=symbol)
    elif bias == "NEUTRAL":
        conclusion = t(lang, "conclusion_neutral", symbol=symbol)
    else:
        conclusion = t(lang, "conclusion_bearish", symbol=symbol)

    supportive_text = ""
    limiting_text = ""

    if supportive_signals:
        supportive_text = t(lang, "supportive_signals") + "\n- " + "\n- ".join(supportive_signals)
    if limiting_factors:
        limiting_text = t(lang, "limiting_factors") + "\n- " + "\n- ".join(limiting_factors)

    analysis = f"""
{t(lang, "technical_summary", symbol=symbol)}

{distance_text}

{supportive_text}

{limiting_text}

{rsi_text}

{t(lang, "conclusion_title")}
{conclusion}
""".strip()

    return analysis, score, bias


def render_sentiment_scale(score: int, bias: str, lang: str) -> None:
    marker_position = max(2, min(98, score))

    bias_class_map = {
        "BULLISH": "bias-bullish",
        "WATCH": "bias-watch",
        "NEUTRAL": "bias-neutral",
        "BEARISH": "bias-bearish",
    }

    bias_class = bias_class_map.get(bias, "bias-neutral")
    localized_bias = local_bias(lang, bias)

    html = f"""
    <div class="scale-wrapper">
        <div class="scale-label">{t(lang, "scale_label")}</div>
        <div class="scale-bar">
            <div class="scale-marker" style="left: {marker_position}%;"></div>
        </div>
        <div class="scale-footer">
            <span>{t(lang, "bearish")}</span>
            <span>{t(lang, "neutral")}</span>
            <span>{t(lang, "bullish")}</span>
        </div>
        <div class="bias-pill {bias_class}">{localized_bias} • {t(lang, "technical_score")}: {score}/100</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def scan_stocks(symbols: list[str], lang: str) -> pd.DataFrame:
    results = []

    progress_bar = st.progress(0)
    status_text = st.empty()
    total = len(symbols)

    for index, symbol in enumerate(symbols, start=1):
        try:
            status_text.text(f"Scanning {symbol} ({index}/{total})...")
            result = get_stock_data(symbol)

            if result and result["AboveMA150"]:
                results.append(
                    {
                        "Symbol": result["Symbol"],
                        "Close": result["Close"],
                        "MA150": result["MA150"],
                        "% Above MA150": result["DifferencePct"],
                    }
                )
        except Exception:
            pass

        progress_bar.progress(index / total)

    status_text.text(t(lang, "scan_complete"))

    df = pd.DataFrame(results)

    if not df.empty:
        df = df.sort_values(by="% Above MA150", ascending=False).reset_index(drop=True)

    return df


st.markdown(f'<div class="app-title">{t(lang, "app_title")}</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="app-subtitle">{t(lang, "app_subtitle")}</div>',
    unsafe_allow_html=True,
)

tab1, tab2 = st.tabs([t(lang, "scanner_tab"), t(lang, "ticker_tab")])


with tab1:
    st.markdown(f'<div class="section-title">{t(lang, "stock_scanner")}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="small-text">{t(lang, "scanner_desc")}</div>',
        unsafe_allow_html=True,
    )

    try:
        symbols = load_symbols("symbols.csv")
    except Exception as e:
        st.error(t(lang, "failed_symbols", error=e))
        st.stop()

    col1, col2, col3 = st.columns(3)
    col1.metric(t(lang, "total_symbols"), len(symbols))
    col2.metric(t(lang, "scan_type"), "MA150")
    col3.metric(t(lang, "mode"), t(lang, "above_only"))

    if st.button(t(lang, "run_scan"), key="run_scan"):
        with st.spinner(t(lang, "scanning_stocks")):
            results_df = scan_stocks(symbols, lang)

        if results_df.empty:
            st.warning(t(lang, "no_stocks_found"))
        else:
            st.success(t(lang, "stocks_found", count=len(results_df)))
            st.caption(t(lang, "sorted_caption"))
            st.dataframe(results_df, use_container_width=True, height=500)

            csv_data = results_df.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                label=t(lang, "download_csv"),
                data=csv_data,
                file_name="ma150_results.csv",
                mime="text/csv",
            )


with tab2:
    st.markdown(f'<div class="section-title">{t(lang, "single_ticker_title")}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="small-text">{t(lang, "single_ticker_desc")}</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([4, 1])

    with left:
        ticker_input = st.text_input(
            t(lang, "ticker"),
            placeholder=t(lang, "ticker_placeholder"),
            label_visibility="collapsed",
        )

    with right:
        analyze_clicked = st.button(t(lang, "analyze_stock"), key="analyze_ticker")

    if analyze_clicked:
        ticker = ticker_input.strip().upper()

        if not ticker or " " in ticker:
            st.error(t(lang, "invalid_ticker"))
        else:
            with st.spinner(t(lang, "checking", ticker=ticker)):
                result = get_stock_data(ticker)

            if result is None:
                st.error(t(lang, "unable_fetch"))
            else:
                c1, c2, c3, c4 = st.columns(4)
                c1.metric(t(lang, "ticker"), result["Symbol"])
                c2.metric(t(lang, "close"), result["Close"])
                c3.metric(t(lang, "ma150"), result["MA150"])

                diff_value = result["DifferencePct"]
                diff_label = f"{diff_value}%"
                diff_delta = f"+{diff_value}%" if diff_value > 0 else f"{diff_value}%"

                c4.metric(
                    t(lang, "distance"),
                    diff_label,
                    delta=diff_delta,
                    delta_color="normal",
                )

                if result["AboveMA150"]:
                    st.markdown(
                        f'<div class="status-box-good">{t(lang, "above_ma150", symbol=result["Symbol"])}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="status-box-bad">{t(lang, "below_ma150", symbol=result["Symbol"])}</div>',
                        unsafe_allow_html=True,
                    )

                analysis_text, score, bias = generate_analysis(result, lang)
                render_sentiment_scale(score, bias, lang)

                analysis_class = "analysis-box-he" if lang == "he" else "analysis-box-en"

                st.markdown(
                    f'<div class="analysis-box {analysis_class}">{analysis_text}</div>',
                    unsafe_allow_html=True,
                )