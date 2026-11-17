from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, Count

def get_period_dates(period, date=None):
    """Returns start_date and end_date for given period"""
    if date is None:
        date = timezone.now().date()
    
    if period == 'week':
        start_date = date - timedelta(days=date.weekday())
        end_date = start_date + timedelta(days=6)
    elif period == 'month':
        start_date = date.replace(day=1)
        next_month = start_date + timedelta(days=32)
        end_date = next_month.replace(day=1) - timedelta(days=1)
    elif period == 'quarter':
        quarter_index = (date.month - 1) // 3
        start_month = quarter_index * 3 + 1
        start_date = date.replace(month=start_month, day=1)
        # End month of the quarter
        end_month = start_month + 2
        # Last day of end month
        if end_month == 12:
            end_date = date.replace(month=12, day=31)
        else:
            next_quarter_start = start_date.replace(month=end_month + 1)
            end_date = next_quarter_start - timedelta(days=1)
    elif period == 'year':
        start_date = date.replace(month=1, day=1)
        end_date = date.replace(month=12, day=31)
    else:
        raise ValueError("Period must be 'week', 'month', 'quarter', or 'year'")
    
    return start_date, end_date

def calculate_streak(activities):
    """Calculate current and longest streak from activities"""
    if not activities:
        return {'current_streak': 0, 'longest_streak': 0}
    
    # Get unique dates sorted in descending order
    dates = sorted(set(a.date for a in activities), reverse=True)
    
    if not dates:
        return {'current_streak': 0, 'longest_streak': 0}
    
    # Calculate current streak
    current_streak = 0
    today = timezone.now().date()
    
    for i, date in enumerate(dates):
        expected_date = today - timedelta(days=i)
        if date == expected_date:
            current_streak += 1
        else:
            break
    
    # Calculate longest streak
    longest_streak = 1
    temp_streak = 1
    
    for i in range(len(dates) - 1):
        if (dates[i] - dates[i + 1]).days == 1:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 1
    
    return {
        'current_streak': current_streak,
        'longest_streak': longest_streak,
        'last_activity_date': dates[0] if dates else None
    }
