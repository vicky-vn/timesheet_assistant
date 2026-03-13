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
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: #0d0d0d; color: #f0f0f0; }
    .main-title {
        font-family: 'Space Mono', monospace;
        font-size: 2.4rem; font-weight: 700;
        color: #e8ff47; letter-spacing: -1px; margin-bottom: 0.2rem;
    }
    .subtitle {
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem; color: #777; margin-bottom: 2.5rem; font-weight: 300;
    }
    .picker-label {
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem; color: #777;
        letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0.6rem;
    }
    .picker-dot {
        font-family: 'Space Mono', monospace;
        font-size: 2rem; font-weight: 700; color: #e8ff47;
        display: flex; align-items: flex-end;
        padding-bottom: 0.4rem; line-height: 1;
    }
    .result-box {
        background: linear-gradient(135deg, #1a1a1a, #141414);
        border: 1px solid #e8ff47; border-radius: 12px;
        padding: 2rem 2.5rem; margin-top: 2rem;
        text-align: center; box-shadow: 0 0 40px rgba(232,255,71,0.08);
    }
    .result-label {
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem; color: #777;
        letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0.5rem;
    }
    .result-value {
        font-family: 'Space Mono', monospace;
        font-size: 4rem; font-weight: 700; color: #e8ff47; line-height: 1;
    }
    .result-unit {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.1rem; color: #aaa; margin-top: 0.5rem; font-weight: 300;
    }
    .breakdown-box {
        background: #151515; border: 1px solid #2a2a2a;
        border-radius: 8px; padding: 1.2rem 1.5rem; margin-top: 1rem;
        font-family: 'Space Mono', monospace; font-size: 0.82rem; color: #666;
    }
    .breakdown-row { display: flex; justify-content: space-between; margin: 0.3rem 0; }
    .breakdown-accent { color: #e8ff47; }
    .divider { border: none; border-top: 1px solid #1e1e1e; margin: 2rem 0; }
    .quick-pick-label {
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem; color: #555;
        letter-spacing: 2px; text-transform: uppercase;
        margin-bottom: 0.6rem; margin-top: 1.8rem;
    }
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
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        text-align: center !important;
    }
    .error-box {
        background: #1a0a0a; border: 1px solid #ff4747;
        border-radius: 8px; padding: 1rem 1.5rem; margin-top: 1rem;
        font-family: 'DM Sans', sans-serif; color: #ff6b6b; font-size: 0.9rem;
    }
    div[data-testid="stButton"] button {
        background: #151515 !important; border: 1px solid #2a2a2a !important;
        border-radius: 8px !important; color: #aaa !important;
        font-family: 'Space Mono', monospace !important;
        font-size: 0.72rem !important; padding: 0.45rem 0.4rem !important;
        width: 100% !important; transition: all 0.15s ease !important;
    }
    div[data-testid="stButton"] button:hover {
        border-color: #e8ff47 !important;
        color: #e8ff47 !important;
        background: #1a1a1a !important;
    }
</style>
""", unsafe_allow_html=True)


# --- Constants ---

HOURS = list(range(1, 13))
ALL_MINUTES_RAW = sorted(set(range(0, 60, 5)) | {14, 15, 45})
MINUTES = [f"{m:02d}" for m in ALL_MINUTES_RAW]
PERIODS = ["AM", "PM"]

DEFAULT_SLOTS = [
    {"label": "9:30→7:00PM", "sh": 9, "sm": "30", "sp": "AM", "eh": 7, "em": "00", "ep": "PM"},
    {"label": "9:30→6:45PM", "sh": 9, "sm": "30", "sp": "AM", "eh": 6, "em": "45", "ep": "PM"},
    {"label": "9:30→7:15PM", "sh": 9, "sm": "30", "sp": "AM", "eh": 7, "em": "15", "ep": "PM"},
    {"label": "9:30→7:45PM", "sh": 9, "sm": "30", "sp": "AM", "eh": 7, "em": "45", "ep": "PM"},
    {"label": "9:30→8:14PM", "sh": 9, "sm": "30", "sp": "AM", "eh": 8, "em": "14", "ep": "PM"},
]


# --- Session state init ---

def init_state():
    defaults = {"sh": 9, "sm": "30", "sp": "AM", "eh": 7, "em": "00", "ep": "PM"}
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# --- Slot apply ---

def apply_slot(slot):
    for k in ["sh", "sm", "sp", "eh", "em", "ep"]:
        st.session_state[k] = slot[k]


# --- Helpers ---

def build_time(hour: int, minute: str, period: str) -> datetime:
    return datetime.strptime(f"{hour}:{minute} {period}", "%I:%M %p")


def calculate_diff(start_dt, end_dt, break_minutes=30):
    if end_dt <= start_dt:
        end_dt += timedelta(days=1)
    diff = end_dt - start_dt
    total_minutes = diff.total_seconds() / 60
    result_minutes = total_minutes - break_minutes
    return total_minutes, result_minutes, result_minutes / 60


# --- on_change callbacks to sync widget → state ---

def on_change_sh(): st.session_state["sh"] = st.session_state["_sh"]
def on_change_sm(): st.session_state["sm"] = st.session_state["_sm"]
def on_change_sp(): st.session_state["sp"] = st.session_state["_sp"]
def on_change_eh(): st.session_state["eh"] = st.session_state["_eh"]
def on_change_em(): st.session_state["em"] = st.session_state["_em"]
def on_change_ep(): st.session_state["ep"] = st.session_state["_ep"]


# --- UI ---

st.markdown('<div class="main-title">⏱ Time Diff</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Calculate working hours with break deduction</div>', unsafe_allow_html=True)

# Start picker
st.markdown('<div class="picker-label">🟢 &nbsp; Start Time</div>', unsafe_allow_html=True)
c1, c2, colon1, c3, _ = st.columns([2, 2, 0.4, 2, 2])
with c1:
    st.selectbox("H", HOURS,
        index=HOURS.index(st.session_state["sh"]),
        key="_sh", on_change=on_change_sh, label_visibility="collapsed")
with c2:
    st.selectbox("M", MINUTES,
        index=MINUTES.index(st.session_state["sm"]),
        key="_sm", on_change=on_change_sm, label_visibility="collapsed")
with colon1:
    st.markdown('<div class="picker-dot">:</div>', unsafe_allow_html=True)
with c3:
    st.selectbox("P", PERIODS,
        index=PERIODS.index(st.session_state["sp"]),
        key="_sp", on_change=on_change_sp, label_visibility="collapsed")

st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)

# End picker
st.markdown('<div class="picker-label">🔴 &nbsp; End Time</div>', unsafe_allow_html=True)
d1, d2, colon2, d3, _ = st.columns([2, 2, 0.4, 2, 2])
with d1:
    st.selectbox("H", HOURS,
        index=HOURS.index(st.session_state["eh"]),
        key="_eh", on_change=on_change_eh, label_visibility="collapsed")
with d2:
    st.selectbox("M", MINUTES,
        index=MINUTES.index(st.session_state["em"]),
        key="_em", on_change=on_change_em, label_visibility="collapsed")
with colon2:
    st.markdown('<div class="picker-dot">:</div>', unsafe_allow_html=True)
with d3:
    st.selectbox("P", PERIODS,
        index=PERIODS.index(st.session_state["ep"]),
        key="_ep", on_change=on_change_ep, label_visibility="collapsed")

# --- Quick picks ---

st.markdown('<div class="quick-pick-label">⚡ Quick Pick</div>', unsafe_allow_html=True)
qcols = st.columns(len(DEFAULT_SLOTS))
for i, slot in enumerate(DEFAULT_SLOTS):
    with qcols[i]:
        if st.button(slot["label"], key=f"slot_{i}"):
            apply_slot(slot)
            st.rerun()

# --- Build datetimes ---

start_dt = build_time(st.session_state["sh"], st.session_state["sm"], st.session_state["sp"])
end_dt   = build_time(st.session_state["eh"], st.session_state["em"], st.session_state["ep"])

# --- Result ---

if start_dt == end_dt:
    st.markdown('<div class="error-box">⚠️ Start and end times are identical.</div>', unsafe_allow_html=True)
else:
    total_mins, result_mins, result_hours = calculate_diff(start_dt, end_dt)

    if result_mins <= 0:
        st.markdown('<div class="error-box">⚠️ Result is zero or negative after break deduction. Choose a wider range.</div>', unsafe_allow_html=True)
    else:
        display_val = f"{result_hours:.1f}"
        start_fmt = start_dt.strftime("%I:%M %p").lstrip("0")
        end_fmt   = end_dt.strftime("%I:%M %p").lstrip("0")

        st.markdown(f"""
        <div class="result-box">
            <div class="result-label">Net Working Hours</div>
            <div class="result-value">{display_val}</div>
            <div class="result-unit">hours</div>
        </div>
        """, unsafe_allow_html=True)

        total_h = int(total_mins // 60)
        total_m = int(total_mins % 60)
        net_h   = int(result_mins // 60)
        net_m   = int(result_mins % 60)

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
