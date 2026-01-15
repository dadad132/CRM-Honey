"""
Business Hours Calculator
Calculates working hours between two datetimes, excluding nights and optionally weekends.
"""
from datetime import datetime, timedelta, time
from typing import Optional


def calculate_business_hours(
    start_dt: datetime,
    end_dt: datetime,
    business_start: str = "07:30",
    business_end: str = "16:00",
    exclude_weekends: bool = True
) -> float:
    """
    Calculate the number of business hours between two datetimes.
    
    Args:
        start_dt: Start datetime
        end_dt: End datetime  
        business_start: Start of business hours in HH:MM format (default "07:30")
        business_end: End of business hours in HH:MM format (default "16:00")
        exclude_weekends: If True, Saturday (5) and Sunday (6) are not counted
    
    Returns:
        Number of business hours as a float
    """
    if not start_dt or not end_dt:
        return 0.0
    
    if end_dt <= start_dt:
        return 0.0
    
    # Parse business hours
    try:
        start_h, start_m = map(int, business_start.split(':'))
        end_h, end_m = map(int, business_end.split(':'))
    except (ValueError, AttributeError):
        # Default to 07:30-16:00 if parsing fails
        start_h, start_m = 7, 30
        end_h, end_m = 16, 0
    
    business_start_time = time(start_h, start_m)
    business_end_time = time(end_h, end_m)
    
    # Calculate business hours per day
    daily_business_minutes = (end_h * 60 + end_m) - (start_h * 60 + start_m)
    if daily_business_minutes <= 0:
        return 0.0
    
    total_minutes = 0.0
    current = start_dt
    
    # Iterate day by day
    while current.date() <= end_dt.date():
        # Skip weekends if configured
        if exclude_weekends and current.weekday() >= 5:  # Saturday=5, Sunday=6
            current = datetime.combine(current.date() + timedelta(days=1), datetime.min.time())
            continue
        
        # Determine the working window for this day
        day_start = datetime.combine(current.date(), business_start_time)
        day_end = datetime.combine(current.date(), business_end_time)
        
        # Adjust for actual start/end times
        if current.date() == start_dt.date():
            # First day - start from actual start time (if within business hours)
            effective_start = max(start_dt, day_start)
        else:
            effective_start = day_start
        
        if current.date() == end_dt.date():
            # Last day - end at actual end time (if within business hours)
            effective_end = min(end_dt, day_end)
        else:
            effective_end = day_end
        
        # Calculate minutes for this day
        if effective_end > effective_start and effective_start < day_end and effective_end > day_start:
            # Ensure we're within business hours
            actual_start = max(effective_start, day_start)
            actual_end = min(effective_end, day_end)
            
            if actual_end > actual_start:
                minutes = (actual_end - actual_start).total_seconds() / 60
                total_minutes += minutes
        
        # Move to next day
        current = datetime.combine(current.date() + timedelta(days=1), datetime.min.time())
    
    return round(total_minutes / 60, 1)  # Return hours


def get_business_hours_display(hours: float) -> str:
    """
    Format business hours for display.
    
    Args:
        hours: Number of hours
    
    Returns:
        Formatted string like "2.5h" or "1d 3h"
    """
    if hours < 8:
        return f"{hours}h"
    else:
        days = int(hours // 8)
        remaining_hours = round(hours % 8, 1)
        if remaining_hours > 0:
            return f"{days}d {remaining_hours}h"
        else:
            return f"{days}d"
