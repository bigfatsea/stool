import logging
import threading
import colorlog
import requests
import time
import sys
import hashlib
import os

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


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
    if isinstance(keys, str):
        keys = keys.split('.')

    if keys and isinstance(keys, list):
        for key in keys:
            if dictionary and key in dictionary:
                dictionary = dictionary[key]
            else:
                return default

    return default



# if __name__ == '__main__':
# print_cmd()
# xxx = logging.getLogger('xxx')
# xxx.error('This is a message from the xxx.')
# logger1 = get_colored_logger('worker')
#
# logger = get_colored_logger('worker')
#
# logger1.info('logger1')
#
#
# def worker():
#     """Example worker function to log and print messages."""
#     thread_name = threading.current_thread().name
#     logger.debug("This is a debug message")
#     logger.info("This is an info message")
#     logger.warning("This is a warning message")
#     logger.error("This is an error message")
#     logger.critical("This is a critical message")
#     time.sleep(1 + 0.1 * get_thread_number())
#     printc(f"This is a message from the {thread_name}|{get_thread_number()} thread.")
#
#
# worker()
# time.sleep(0.5)
# logger.info('-' * 30)
#
# with ThreadPoolExecutor(max_workers=2) as executor:
#     for i in range(2):
#         executor.submit(worker)
