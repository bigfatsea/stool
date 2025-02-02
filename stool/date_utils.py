from datetime import datetime, timedelta


def first_day_of_month(any_day):
    """Return the first day of the current month."""
    return any_day.replace(day=1)


def last_day_of_month(any_day):
    """Return the last day of the current month."""
    next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)


def split_into_months(start_date, end_date):
    return generate_time_ranges(start_date, end_date, 'monthly')



def generate_time_ranges(start_date, end_date, interval='monthly'):
    """Generates time ranges based on a given interval.

    Args:
        start_date (str): Start date in "yyyy-MM-dd" format.
        end_date (str): End date in "yyyy-MM-dd" format.
        interval (str or int): Interval specification. Can be:
            - 'yearly'
            - 'quarterly'
            - 'monthly'
            - 'weekly'
            - 'daily'
            - An integer representing a number of days.

    Returns:
        list: List of time ranges, each as a tuple of strings
              (start_date, end_date) in "yyyy-MM-dd" format.
    """

    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    ranges = []

    if interval == 'monthly':
        while start <= end:
            end_of_month = last_day_of_month(start)
            current_end = min(end, end_of_month)
            ranges.append((start.strftime('%Y-%m-%d'), current_end.strftime('%Y-%m-%d')))
            start = current_end + timedelta(days=1)
    elif interval == 'yearly':
        while start <= end:
            end_of_year = start.replace(month=12, day=31)
            current_end = min(end, end_of_year)
            ranges.append((start.strftime('%Y-%m-%d'), current_end.strftime('%Y-%m-%d')))
            start = current_end + timedelta(days=1)
    elif interval == 'quarterly':
        while start <= end:
            if start.month in [1, 2, 3]:
                end_of_quarter = start.replace(month=3, day=31)
            elif start.month in [4, 5, 6]:
                end_of_quarter = start.replace(month=6, day=30)
            elif start.month in [7, 8, 9]:
                end_of_quarter = start.replace(month=9, day=30)
            else:
                end_of_quarter = start.replace(month=12, day=31)
            current_end = min(end, end_of_quarter)
            ranges.append((start.strftime('%Y-%m-%d'), current_end.strftime('%Y-%m-%d')))
            start = current_end + timedelta(days=1)
    else:
        if interval == 'weekly':
            inter = 6
        elif interval == 'daily':
            inter = 0
        elif isinstance(interval, int) or interval.isdigit():
            inter = int(interval) - 1 if int(interval) > 0 else 0
        else:
            ranges.append((start_date, end_date))
            return ranges

        while start <= end:
            current_end = start + timedelta(days=inter)
            current_end = min(end, current_end)
            ranges.append((start.strftime('%Y-%m-%d'), current_end.strftime('%Y-%m-%d')))
            start = current_end + timedelta(days=1)

    return ranges


from dateutil import parser as dateutil_parser
import pytz
from datetime import datetime, timezone, timedelta
import logging

def tz_it(d, tz=None):
    """
    Convert datetime to specified timezone
    Args:
        d: datetime object
        tz: timezone string (e.g., 'UTC', 'Asia/Shanghai')
    Returns:
        datetime object with specified timezone
    """
    if not d:
        return d

    if not isinstance(d, datetime):
        raise TypeError(f"Expected datetime object, got {type(d)}")

    tzz = timezone.utc
    if isinstance(tz, str):
        try:
            tzz = pytz.timezone(tz)
        except Exception as e:
            logging.exception(f"Failed to get timezone {tz}: {e}")

    # Ensure datetime has tzinfo
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)

    return d.astimezone(tzz)


def parse_date(date_str, date_format=None):
    """解析日期字符串为 datetime 对象"""
    if not date_str:
        return None

    if date_format:
        try:
            date_obj = datetime.strptime(date_str, date_format)
            return tz_it(date_obj)
        except Exception as e:
            logging.warning(f"Failed to parse date string {date_str} with format {date_format}: {e}")

    try:
        date_obj = dateutil_parser.parse(date_str)
        return tz_it(date_obj)
    except Exception as e:
        logging.exception(f"Failed to parse date string {date_str}: {e}")

    return None
