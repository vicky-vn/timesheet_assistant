# ⏱ Time Difference Calculator

A clean Streamlit app that calculates net working hours and overtime beyond a selected scheduled end, while automatically deducting a 30-minute break from net hours.

## Example
- **Scheduled start:** 9:00 AM
- **Scheduled end:** 6:15 PM
- **Actual end:** 7:00 PM
- **Gross:** 10 hours
- **Minus break:** − 30 min  
- **Net result:** **9.5 hours**
- **Overtime:** **0h 45m** ✅

## Features
- Dropdown selectors in 5-minute increments
- Configurable scheduled start, scheduled end, and actual end
- Quick timing presets for common day and afternoon shifts
- Overtime presets that apply relative to the selected schedule
- Overtime shown for work beyond the scheduled end
- Overnight shift support (e.g. 10 PM → 6 AM)
- Result shown as float (e.g. `9.5`, `7.75`)
- Full breakdown (gross time, deduction, net hours)

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push this repo to GitHub (public)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → connect your GitHub repo
4. Set **Main file path** to `app.py`
5. Click **Deploy** 🚀

## Project Structure

```
time-diff-app/
├── app.py            # Main Streamlit application
├── requirements.txt  # Python dependencies
└── README.md         # This file
```
