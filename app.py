import streamlit as st
from datetime import datetime, timedelta

from time_utils import calculate_diff, calculate_overtime, format_hours

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
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 0.5rem !important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        flex: 1 1 0 !important;
        min-width: 0 !important;
        width: 0 !important;
    }
    .error-box {
        background: #1a0a0a; border: 1px solid #ff4747;
        border-radius: 8px; padding: 1rem 1.5rem; margin-top: 1rem;
        font-family: 'DM Sans', sans-serif; color: #ff6b6b; font-size: 0.9rem;
    }

    /* Default quick pick button */
    div[data-testid="stButton"] button {
        background: #151515 !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 8px !important;
        color: #666 !important;
        font-family: 'Space Mono', monospace !important;
        font-size: 0.72rem !important;
        padding: 0.45rem 0.4rem !important;
        width: 100% !important;
        transition: all 0.15s ease !important;
    }
    div[data-testid="stButton"] button:hover {
        border-color: #e8ff47 !important;
        color: #e8ff47 !important;
        background: #1a1a1a !important;
    }

    /* Active quick pick button */
    div[data-testid="stButton"] button[data-testid="stBaseButton-primary"] {
        background: #1f2200 !important;
        border: 1px solid #e8ff47 !important;
        color: #e8ff47 !important;
        box-shadow: 0 0 12px rgba(232, 255, 71, 0.15) !important;
    }
</style>
""", unsafe_allow_html=True)


# --- Constants ---

HOURS = list(range(1, 13))
MINUTES = [f"{m:02d}" for m in range(0, 60, 5)]
PERIODS = ["AM", "PM"]

TIMING_SLOTS = [
    {"label": "9–6:15", "sh": 9, "sm": "00", "sp": "AM", "seh": 6, "sem": "15", "sep": "PM"},
    {"label": "9–6:30", "sh": 9, "sm": "00", "sp": "AM", "seh": 6, "sem": "30", "sep": "PM"},
    {"label": "1–10:30", "sh": 1, "sm": "00", "sp": "PM", "seh": 10, "sem": "30", "sep": "PM"},
    {"label": "1:15–10:30", "sh": 1, "sm": "15", "sp": "PM", "seh": 10, "sem": "30", "sep": "PM"},
    {"label": "8–5:30", "sh": 8, "sm": "00", "sp": "AM", "seh": 5, "sem": "30", "sep": "PM"},
    {"label": "8–5:15", "sh": 8, "sm": "00", "sp": "AM", "seh": 5, "sem": "15", "sep": "PM"},
]

OVERTIME_SLOTS = [
    {"label": "0m OT", "minutes": 0},
    {"label": "30m OT", "minutes": 30},
    {"label": "1h OT", "minutes": 60},
    {"label": "1h30 OT", "minutes": 90},
    {"label": "2h OT", "minutes": 120},
]


# --- Session state init ---

def init_state():
    defaults = {
        "sh": 9, "sm": "00", "sp": "AM",
        "seh": 6, "sem": "15", "sep": "PM",
        "eh": 6, "em": "15", "ep": "PM",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    if "picker_version" not in st.session_state:
        st.session_state["picker_version"] = 0

init_state()


# --- Helpers ---

def apply_timing_slot(slot):
    for k in ["sh", "sm", "sp", "seh", "sem", "sep"]:
        st.session_state[k] = slot[k]
    st.session_state["eh"] = slot["seh"]
    st.session_state["em"] = slot["sem"]
    st.session_state["ep"] = slot["sep"]
    st.session_state["picker_version"] += 1


def is_active_timing_slot(slot):
    keys = ["sh", "sm", "sp", "seh", "sem", "sep"]
    return all(st.session_state[k] == slot[k] for k in keys)


def build_time(hour: int, minute: str, period: str) -> datetime:
    return datetime.strptime(f"{hour}:{minute} {period}", "%I:%M %p")


def actual_end_for_overtime(overtime_minutes):
    scheduled_end = build_time(
        st.session_state["seh"],
        st.session_state["sem"],
        st.session_state["sep"],
    )
    return scheduled_end + timedelta(minutes=overtime_minutes)


def apply_overtime_slot(overtime_minutes):
    actual_end = actual_end_for_overtime(overtime_minutes)
    st.session_state["eh"] = int(actual_end.strftime("%I"))
    st.session_state["em"] = actual_end.strftime("%M")
    st.session_state["ep"] = actual_end.strftime("%p")
    st.session_state["picker_version"] += 1


def is_active_overtime_slot(overtime_minutes):
    actual_end = actual_end_for_overtime(overtime_minutes)
    return (
        st.session_state["eh"] == int(actual_end.strftime("%I"))
        and st.session_state["em"] == actual_end.strftime("%M")
        and st.session_state["ep"] == actual_end.strftime("%p")
    )


# --- on_change callbacks ---

def on_change_sh(): st.session_state["sh"] = st.session_state[f"_sh_{st.session_state['picker_version']}"]
def on_change_sm(): st.session_state["sm"] = st.session_state[f"_sm_{st.session_state['picker_version']}"]
def on_change_sp(): st.session_state["sp"] = st.session_state[f"_sp_{st.session_state['picker_version']}"]
def on_change_seh(): st.session_state["seh"] = st.session_state[f"_seh_{st.session_state['picker_version']}"]
def on_change_sem(): st.session_state["sem"] = st.session_state[f"_sem_{st.session_state['picker_version']}"]
def on_change_sep(): st.session_state["sep"] = st.session_state[f"_sep_{st.session_state['picker_version']}"]
def on_change_eh(): st.session_state["eh"] = st.session_state[f"_eh_{st.session_state['picker_version']}"]
def on_change_em(): st.session_state["em"] = st.session_state[f"_em_{st.session_state['picker_version']}"]
def on_change_ep(): st.session_state["ep"] = st.session_state[f"_ep_{st.session_state['picker_version']}"]


# --- UI ---

st.markdown('<div class="main-title">⏱ Time Diff</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Net hours plus overtime beyond your scheduled end</div>', unsafe_allow_html=True)

v = st.session_state["picker_version"]

# Scheduled start picker
st.markdown('<div class="picker-label">🟢 &nbsp; Scheduled Start</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.selectbox("H", HOURS,
        index=HOURS.index(st.session_state["sh"]),
        key=f"_sh_{v}", on_change=on_change_sh, label_visibility="collapsed")
with c2:
    st.selectbox("M", MINUTES,
        index=MINUTES.index(st.session_state["sm"]),
        key=f"_sm_{v}", on_change=on_change_sm, label_visibility="collapsed")
with c3:
    st.selectbox("P", PERIODS,
        index=PERIODS.index(st.session_state["sp"]),
        key=f"_sp_{v}", on_change=on_change_sp, label_visibility="collapsed")

st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)

# Scheduled end picker
st.markdown('<div class="picker-label">🟡 &nbsp; Scheduled End</div>', unsafe_allow_html=True)
s1, s2, s3 = st.columns(3)
with s1:
    st.selectbox("H", HOURS,
        index=HOURS.index(st.session_state["seh"]),
        key=f"_seh_{v}", on_change=on_change_seh, label_visibility="collapsed")
with s2:
    st.selectbox("M", MINUTES,
        index=MINUTES.index(st.session_state["sem"]),
        key=f"_sem_{v}", on_change=on_change_sem, label_visibility="collapsed")
with s3:
    st.selectbox("P", PERIODS,
        index=PERIODS.index(st.session_state["sep"]),
        key=f"_sep_{v}", on_change=on_change_sep, label_visibility="collapsed")

st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)

# Actual end picker
st.markdown('<div class="picker-label">🔴 &nbsp; Actual End</div>', unsafe_allow_html=True)
d1, d2, d3 = st.columns(3)
with d1:
    st.selectbox("H", HOURS,
        index=HOURS.index(st.session_state["eh"]),
        key=f"_eh_{v}", on_change=on_change_eh, label_visibility="collapsed")
with d2:
    st.selectbox("M", MINUTES,
        index=MINUTES.index(st.session_state["em"]),
        key=f"_em_{v}", on_change=on_change_em, label_visibility="collapsed")
with d3:
    st.selectbox("P", PERIODS,
        index=PERIODS.index(st.session_state["ep"]),
        key=f"_ep_{v}", on_change=on_change_ep, label_visibility="collapsed")

# --- Timing and overtime quick picks ---

st.markdown('<div class="quick-pick-label">🕒 Actual Timing</div>', unsafe_allow_html=True)
tcols = st.columns(len(TIMING_SLOTS))
for i, slot in enumerate(TIMING_SLOTS):
    with tcols[i]:
        active = is_active_timing_slot(slot)
        if st.button(
            slot["label"],
            key=f"timing_slot_{i}",
            type="primary" if active else "secondary",
        ):
            apply_timing_slot(slot)
            st.rerun()

st.markdown('<div class="quick-pick-label">⚡ Overtime</div>', unsafe_allow_html=True)
qcols = st.columns(len(OVERTIME_SLOTS))
for i, slot in enumerate(OVERTIME_SLOTS):
    with qcols[i]:
        active = is_active_overtime_slot(slot["minutes"])
        if st.button(
            slot["label"],
            key=f"overtime_slot_{i}",
            type="primary" if active else "secondary",
        ):
            apply_overtime_slot(slot["minutes"])
            st.rerun()

# --- Build datetimes ---

start_dt = build_time(st.session_state["sh"], st.session_state["sm"], st.session_state["sp"])
scheduled_end_dt = build_time(st.session_state["seh"], st.session_state["sem"], st.session_state["sep"])
end_dt = build_time(st.session_state["eh"], st.session_state["em"], st.session_state["ep"])

# --- Result ---

if start_dt == end_dt:
    st.markdown('<div class="error-box">⚠️ Start and end times are identical.</div>', unsafe_allow_html=True)
else:
    total_mins, result_mins, result_hours = calculate_diff(start_dt, end_dt)

    if result_mins <= 0:
        st.markdown('<div class="error-box">⚠️ Result is zero or negative after break deduction. Choose a wider range.</div>', unsafe_allow_html=True)
    else:
        overtime_mins = calculate_overtime(start_dt, scheduled_end_dt, end_dt)
        overtime_h = overtime_mins // 60
        overtime_m = overtime_mins % 60
        display_val = format_hours(result_hours)
        start_fmt = start_dt.strftime("%I:%M %p").lstrip("0")
        scheduled_end_fmt = scheduled_end_dt.strftime("%I:%M %p").lstrip("0")
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
                <span>Scheduled end</span>
                <span class="breakdown-accent">{scheduled_end_fmt}</span>
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
            <div class="breakdown-row">
                <span>Overtime</span>
                <span class="breakdown-accent">{overtime_h}h {overtime_m:02d}m</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)
