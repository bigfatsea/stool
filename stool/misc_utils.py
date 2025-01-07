import functools
import hashlib
import json
import logging
import os
import requests
import sys
import warnings
from datetime import datetime, timedelta
from typing import Dict, List


def deprecated(reason=''):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(f"{func.__name__} is deprecated and will be removed in a future version. {reason}",
                          category=DeprecationWarning,
                          stacklevel=2)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def expand_config_file(file):
    code_file_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(code_file_dir, file)


def expand_dir(dir):
    return os.path.expanduser(dir) if dir.startswith('~') else os.path.abspath(dir)


def file_exists_and_not_empty(file_path: str, min_size: int = 100) -> bool:
    return os.path.exists(file_path) and os.path.getsize(file_path) > min_size


def save_json(data, file_path: str) -> None:
    logging.info(f'Saving data to {file_path}')
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(file_path: str):
    logging.info(f'Loading data from {file_path}')
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def send_msg(message, title=None):
    title = title or f"{os.path.basename(sys.argv[0])} {' '.join(sys.argv[1:])}"
    url = f"https://api.day.app/vFVZRfhJbEsiT9XndGYpf5/{title}/{message}"
    requests.get(url)


def get_md5(url):
    """Return MD5 hash of the URL."""
    return hashlib.md5(url.encode('utf-8')).hexdigest()


def del_by_size(directory, ext='.html', min_size=3 * 1024):
    total = 0
    total_size = 0
    deleted = 0
    deleted_size = 0
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path) and file_path.endswith(ext):
                total += 1
                file_size = os.path.getsize(file_path)
                total_size += file_size
                if file_size < min_size:
                    deleted += 1
                    deleted_size += file_size
                    os.remove(file_path)
    return total, total_size, deleted, deleted_size


def exclude_keyword(data: Dict, excluded_keyword: str, mask=None) -> Dict:
    if not excluded_keyword:
        return data
    if mask:
        return {k: (v if excluded_keyword not in k else mask) for k, v in data.items()}
    else:
        return {k: v for k, v in data.items() if excluded_keyword not in k}


def exclude_keys(data: Dict, excluded_keys: List, mask=None) -> Dict:
    if not excluded_keys:
        return data
    if mask:
        return {k: (v if k not in excluded_keys else mask) for k, v in data.items()}
    else:
        return {k: v for k, v in data.items() if k not in excluded_keys}


def reserve_keyword(data: Dict, reserved_keyword: str) -> Dict:
    return {k: v for k, v in data.items() if reserved_keyword in k} if reserved_keyword else data


def reserve_keys(data: Dict, reserved_keys: List) -> Dict:
    return {k: v for k, v in data.items() if k in reserved_keys} if reserved_keys else data


def deep_get(dictionary, keys, default=None):
    if not dictionary:
        return default

    if isinstance(keys, str):
        keys = keys.split('.')

    if keys and isinstance(keys, list):
        for key in keys:
            if isinstance(dictionary, dict) and key in dictionary:
                dictionary = dictionary[key]
            else:
                return default
        return dictionary if None != dictionary else default

    return default


# custom_json_encoder.py


class CustomJSONEncoder(json.JSONEncoder):
    """
    A customizable JSON encoder that formats floats, datetimes, and timedeltas.

    Formatting:
    - Floats are rounded to two decimal places.
    - Datetimes are formatted as "YYYY-MM-DD HH:MM:SS".
    - Timedeltas are formatted as "hh:mm:ss.SSS" where:
        - hh can exceed 24 to represent total hours.
        - mm represents minutes.
        - ss represents seconds.
        - SSS represents milliseconds.
    """

    float_format = '.2f'  # Default: 2 decimal places
    datetime_format = "%Y-%m-%d %H:%M:%S"  # Default datetime format
    timedelta_format = "hh:mm:ss.SSS"  # Default timedelta format

    def default(self, obj):
        if isinstance(obj, float):
            # Round float to two decimal places
            return round(obj, 2)
        elif isinstance(obj, datetime):
            # Format datetime using the specified format
            return obj.strftime(self.datetime_format)
        elif isinstance(obj, timedelta):
            # Format timedelta to "hh:mm:ss.SSS"
            total_seconds = obj.total_seconds()
            is_negative = total_seconds < 0
            total_seconds = abs(total_seconds)

            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)
            milliseconds = int(round((total_seconds - int(total_seconds)) * 1000))

            formatted_timedelta = f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

            if is_negative:
                formatted_timedelta = f"-{formatted_timedelta}"

            return formatted_timedelta
        return super().default(obj)


if __name__ == '__main__':
    data = {
        'price': 123.456789,
        'timestamp': datetime(2024, 10, 19, 16, 45, 30),
        'duration': timedelta(hours=12, minutes=31, seconds=45, microseconds=123000),
        'description': 'Sample product',
        'metrics': {
            'accuracy': 0.987654321,
            'last_updated': datetime.now(),
        },
        'values': [1.2345, 6.7890, 3.14159],
        'short_duration': timedelta(minutes=12, seconds=31),
        'long_duration': timedelta(hours=123, minutes=12, seconds=1),
        'negative_duration': -timedelta(hours=1, minutes=45, seconds=30, microseconds=456000),
    }

    # Serialize data using the CustomJSONEncoder
    json_str = json.dumps(data, cls=CustomJSONEncoder, indent=2)
    print(json_str)
