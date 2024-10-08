import functools
import hashlib
import json
import logging
import os
import sys
import warnings

import requests


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
