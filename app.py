import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Time Difference Calculator",
    page_icon="⏱️",
    layout="centered"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: #0d0d0d;
        color: #f0f0f0;
    }

    .main-title {
        font-family: 'Space Mono', monospace;
        font-size: 2.4rem;
        font-weight: 700;
        color: #e8ff47;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
        color: #777;
        margin-bottom: 2.5rem;
        font-weight: 300;
    }

    .picker-label {
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        color: #777;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }

    .picker-wrapper {
        background: #151515;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 1.2rem 1.5rem 1.5rem 1.5rem;
        margin-bottom: 1rem;
    }

    .picker-dot {
        font-family: 'Space Mono', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: #e8ff47;
        display: flex;
        align-items: flex-end;
        padding-bottom: 0.4rem;
        line-height: 1;
    }

    .result-box {
        background: linear-gradient(135deg, #1a1a1a, #141414);
        border: 1px solid #e8ff47;
        border-radius: 12px;
        padding: 2rem 2.5rem;
        margin-top: 2rem;
        text-align: center;
        box-shadow: 0 0 40px rgba(232, 255, 71, 0.08);
    }

    .result-label {
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        color: #777;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .result-value {
        font-family: 'Space Mono', monospace;
        font-size: 4rem;
        font-weight: 700;
        color: #e8ff47;
        line-height: 1;
    }

    .result-unit {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.1rem;
        color: #aaa;
        margin-top: 0.5rem;
        font-weight: 300;
    }

    .breakdown-box {
        background: #151515;
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        margin-top: 1rem;
        font-family: 'Space Mono', monospace;
        font-size: 0.82rem;
        color: #666;
    }

    .breakdown-row {
        display: flex;
        justify-content: space-between;
        margin: 0.3rem 0;
    }

    .breakdown-accent {
        color: #e8ff47;
    }

    .divider {
        border: none;
        border-top: 1px solid #1e1e1e;
        margin: 2rem 0;
    }

    /* Selectbox overrides */
    div[data-testid="stSelectbox"] > label {
        color: #666 !important;
        font-family: 'Space Mono', monospace !important;
        font-size: 0.7rem !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }

    div[data-testid="stSelectbox"] > div > div {
        background-color: #1e1e1e !important;
        border: 1px solid #333 !important;
        color: #f0f0f0 !important;
        border-radius: 8px !important;
        font-family: 'Space Mono', monospace !important;
        font-size: 1.0rem !important;
        font-weight: 700 !important;
        text-align: center !important;
    }

    .error-box {
        background: #1a0a0a;
        border: 1px solid #ff4747;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin-top: 1rem;
        font-family: 'DM Sans', sans-serif;
        color: #ff6b6b;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


def build_time(hour: int, minute: int, period: str) -> datetime:
    """Construct a datetime from picker values."""
    time_str = f"{hour}:{minute:02d} {period}"
    return datetime.strptime(time_str, "%I:%M %p")


def calculate_diff(start_dt, end_dt, break_minutes=30):
    """Calculate time difference minus break, return hours as float."""
    if end_dt <= start_dt:
        end_dt += timedelta(days=1)
    diff = end_dt - start_dt
    total_minutes = diff.total_seconds() / 60
    result_minutes = total_minutes - break_minutes
    return total_minutes, result_minutes, result_minutes / 60


# --- UI ---

st.markdown('<div class="main-title">⏱ Time Diff</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Calculate working hours with break deduction</div>', unsafe_allow_html=True)

HOURS = list(range(1, 13))           # 1 – 12
MINUTES = [f"{m:02d}" for m in range(0, 60, 5)]   # 00, 05, 10 … 55
PERIODS = ["AM", "PM"]

# --- Start Time Picker ---
st.markdown('<div class="picker-label">🟢 &nbsp; Start Time</div>', unsafe_allow_html=True)
with st.container():
    c1, c2, colon_col, c3, c4 = st.columns([2, 2, 0.5, 2, 2])
    with c1:
        start_hour = st.selectbox("Hour", HOURS, index=HOURS.index(10), key="sh", label_visibility="collapsed")
    with c2:
        start_min = st.selectbox("Min", MINUTES, index=0, key="sm", label_visibility="collapsed")
    with colon_col:
        st.markdown('<div class="picker-dot">:</div>', unsafe_allow_html=True)
    with c3:
        start_period = st.selectbox("AM/PM", PERIODS, index=0, key="sp", label_visibility="collapsed")
    with c4:
        st.empty()  # spacer to keep visual balance

st.markdown("<div style='margin-top: 1.2rem'></div>", unsafe_allow_html=True)

# --- End Time Picker ---
st.markdown('<div class="picker-label">🔴 &nbsp; End Time</div>', unsafe_allow_html=True)
with st.container():
    d1, d2, colon_col2, d3, d4 = st.columns([2, 2, 0.5, 2, 2])
    with d1:
        end_hour = st.selectbox("Hour", HOURS, index=HOURS.index(8), key="eh", label_visibility="collapsed")
    with d2:
        end_min = st.selectbox("Min", MINUTES, index=0, key="em", label_visibility="collapsed")
    with colon_col2:
        st.markdown('<div class="picker-dot">:</div>', unsafe_allow_html=True)
    with d3:
        end_period = st.selectbox("AM/PM", PERIODS, index=1, key="ep", label_visibility="collapsed")
    with d4:
        st.empty()

# --- Build datetimes ---
start_dt = build_time(start_hour, int(start_min), start_period)
end_dt = build_time(end_hour, int(end_min), end_period)

# --- Same time guard ---
if start_dt == end_dt:
    st.markdown("""
    <div class="error-box">
        ⚠️ Start and end times are identical. Please select a different end time.
    </div>
    """, unsafe_allow_html=True)
else:
    total_mins, result_mins, result_hours = calculate_diff(start_dt, end_dt)

    if result_mins <= 0:
        st.markdown("""
        <div class="error-box">
            ⚠️ The result is zero or negative after subtracting the 30-minute break.
            Please choose a wider time range.
        </div>
        """, unsafe_allow_html=True)
    else:
        display_val = f"{result_hours:.1f}"

        start_fmt = start_dt.strftime("%I:%M %p").lstrip("0")
        end_fmt = end_dt.strftime("%I:%M %p").lstrip("0")

        st.markdown(f"""
        <div class="result-box">
            <div class="result-value">{display_val}</div>
            <div class="result-unit">hours</div>
        </div>
        """, unsafe_allow_html=True)

        total_h = int(total_mins // 60)
        total_m = int(total_mins % 60)
        net_h = int(result_mins // 60)
        net_m = int(result_mins % 60)

        st.markdown(f"""
        <div class="breakdown-box">
            <div class="breakdown-row">
                <span>Start → End</span>
                <span class="breakdown-accent">{start_fmt} → {end_fmt}</span>
            </div>
            <div class="breakdown-row">
                <span>Gross duration</span>
                <span class="breakdown-accent">{total_h}h {total_m:02d}m</span>
            </div>
            <div class="breakdown-row">
                <span>Break deducted</span>
                <span style="color:#ff6b6b;">− 30 min</span>
            </div>
            <div class="breakdown-row">
                <span>Net time</span>
                <span class="breakdown-accent">{net_h}h {net_m:02d}m = {result_hours:.4f} hrs</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)
# st.markdown('<p style="color:#333; font-size:0.75rem; text-align:center; font-family: Space Mono, monospace;">30-min break auto-deducted · overnight shifts supported</p>', unsafe_allow_html=True)
