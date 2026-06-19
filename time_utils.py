from datetime import timedelta


def calculate_diff(start_dt, end_dt, break_minutes=30):
    if end_dt <= start_dt:
        end_dt += timedelta(days=1)
    diff = end_dt - start_dt
    total_minutes = diff.total_seconds() / 60
    result_minutes = total_minutes - break_minutes
    return total_minutes, result_minutes, result_minutes / 60


def calculate_overtime(start_dt, scheduled_end_dt, actual_end_dt):
    """Return minutes worked after the scheduled end on the shift timeline."""
    if scheduled_end_dt <= start_dt:
        scheduled_end_dt += timedelta(days=1)
    if actual_end_dt <= start_dt:
        actual_end_dt += timedelta(days=1)
    return max(0, int((actual_end_dt - scheduled_end_dt).total_seconds() / 60))


def format_hours(hours):
    """Show quarter-hour precision without unnecessary trailing zeroes."""
    return f"{hours:.2f}".rstrip("0").rstrip(".")
