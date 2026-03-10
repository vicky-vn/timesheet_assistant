# ⏱ Time Difference Calculator

A clean Streamlit app that calculates net working hours between two times, automatically deducting a 30-minute break.

## Example
- **Start:** 10:00 AM  
- **End:** 8:00 PM  
- **Gross:** 10 hours  
- **Minus break:** − 30 min  
- **Result:** **9.5 hours** ✅

## Features
- Dropdown selectors in 30-minute increments
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