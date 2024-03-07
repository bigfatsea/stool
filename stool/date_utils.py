from datetime import datetime, timedelta


def first_day_of_month(any_day):
    """Return the first day of the current month."""
    return any_day.replace(day=1)


def last_day_of_month(any_day):
    """Return the last day of the current month."""
    next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)


def split_into_months(start_date, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    ranges = []

    while start < end:
        # Determine the last day of the month for the current 'start'
        end_of_month = last_day_of_month(start)
        # If the end_of_month is after the 'end', use 'end' instead
        current_end = min(end, end_of_month)
        # Add the current range to the list
        ranges.append((start.strftime('%Y-%m-%d'), current_end.strftime('%Y-%m-%d')))
        # Set the new start to be the day after the current_end
        start = current_end + timedelta(days=1)

    return ranges
