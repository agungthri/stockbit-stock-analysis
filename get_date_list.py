import holidays
from datetime import datetime, timedelta

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")

def is_valid_business_day(date, holidays):
    return date.weekday() < 5 and date not in holidays

def get_business_dates(start_date, end_date, holidays):
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        if is_valid_business_day(current_date, holidays):
            date_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    return date_list

def get_date_list(start_date_str, end_date_str):
    start_date = parse_date(start_date_str)
    end_date = parse_date(end_date_str)
    id_holidays = holidays.Indonesia()
    return get_business_dates(start_date, end_date, id_holidays)
