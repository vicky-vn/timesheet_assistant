import streamlit as st
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Time Difference Calculator",
    page_icon="⏱️",
    layout="centered"
)

# Custom CSS
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

    /* Override Streamlit input styles */
    .stSelectbox > div > div {
        background-color: #1a1a1a !important;
        border: 1px solid #2a2a2a !important;
        color: #f0f0f0 !important;
        border-radius: 8px !important;
        font-family: 'Space Mono', monospace !important;
    }

    .stSelectbox label {
        color: #aaa !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.9rem !important;
        font-weight: 400 !important;
    }

    div[data-testid="stSelectbox"] > label {
        color: #aaa !important;
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


FORMATS = [
    "%I:%M %p",   # 10:07 AM
    "%I:%M%p",    # 10:07AM
    "%H:%M",      # 22:07
    "%I %p",      # 10 AM
    "%I%p",       # 10AM
    "%H",         # 22
]


def parse_time(raw: str):
    """Try multiple formats; return datetime or None."""
    raw = raw.strip()
    for fmt in FORMATS:
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    return None


def calculate_diff(start_dt, end_dt, break_minutes=30):
    """Calculate time difference minus break, return hours as float."""
    if end_dt <= start_dt:
        end_dt += timedelta(days=1)  # Handle overnight shifts
    diff = end_dt - start_dt
    total_minutes = diff.total_seconds() / 60
    result_minutes = total_minutes - break_minutes
    return total_minutes, result_minutes, result_minutes / 60


# --- UI ---

st.markdown('<div class="main-title">⏱ Time Diff</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Calculate working hours with break deduction</div>', unsafe_allow_html=True)

st.markdown(
    '<p style="color:#555; font-size:0.8rem; font-family: Space Mono, monospace; margin-bottom:1.2rem;">'
    'Accepted formats: &nbsp;<span style="color:#e8ff47">10:07 AM &nbsp;·&nbsp; 9:45 PM &nbsp;·&nbsp; 14:30 &nbsp;·&nbsp; 10AM</span>'
    '</p>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    start_raw = st.text_input("🟢 Start Time", value="10:00 AM", placeholder="e.g. 9:17 AM")

with col2:
    end_raw = st.text_input("🔴 End Time", value="8:00 PM", placeholder="e.g. 6:45 PM")

start_dt = parse_time(start_raw)
end_dt = parse_time(end_raw)

if not start_dt:
    st.markdown(f'<div class="error-box">⚠️ Could not parse start time: <b>"{start_raw}"</b><br>Try formats like <code>9:17 AM</code>, <code>14:30</code>, or <code>10AM</code></div>', unsafe_allow_html=True)
elif not end_dt:
    st.markdown(f'<div class="error-box">⚠️ Could not parse end time: <b>"{end_raw}"</b><br>Try formats like <code>6:45 PM</code>, <code>18:00</code>, or <code>8PM</code></div>', unsafe_allow_html=True)
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
        display_val = f"{result_hours:.1f}" if result_hours != int(result_hours) else f"{int(result_hours)}.0"

        start_fmt = start_dt.strftime("%I:%M %p").lstrip("0")
        end_fmt = end_dt.strftime("%I:%M %p").lstrip("0")

        st.markdown(f"""
        <div class="result-box">
            <div class="result-label">Net Working Hours</div>
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
st.markdown('<p style="color:#333; font-size:0.75rem; text-align:center; font-family: Space Mono, monospace;">30-min break auto-deducted · overnight shifts supported</p>', unsafe_allow_html=True)