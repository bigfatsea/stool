import logging
import os
import sys
import threading
import time

import colorlog
from colorama import Fore

from stool.misc_utils import deprecated

# Thread-specific colors
# _THREAD_COLORS = [34, 36, 32, 33, 31, 35]
_THREAD_COLORS = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.MAGENTA]
_RESET_COLOR = Fore.RESET


# convert seconds into hh:mm:ss
def sec2str(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}"


def sec2str_hms(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{int(h):d}h {int(m):d}m {int(s):d}s"


def get_thread_number():
    """Get the thread number."""
    thread_name = threading.current_thread().name
    n = ''.join(filter(str.isdigit, thread_name.split('-')[-1]))
    return int(n) if n.isdigit() else -1


def _get_thread_color():
    """Get color based on the thread number."""
    thread_number = get_thread_number()
    return Fore.WHITE if thread_number < 0 else _THREAD_COLORS[thread_number % len(_THREAD_COLORS)]


def print_cmd():
    header = 'START @ ' + time.strftime("%Y-%m-%d %H:%M:%S")
    cmd = f"{os.path.basename(sys.argv[0])} {' '.join(sys.argv[1:])}"
    print(f"\n{header:-^80}\n {cmd}\n{'-' * 80}", flush=True)


def printc(*messages, **kwargs):
    """
    Print colored messages based on the thread number.
    Each message will be printed on a new line.

    :param messages: Any number of messages to be printed.
    :param kwargs: Keyword arguments that could be passed to the print function.
    """
    color = _get_thread_color()
    reset_color = _RESET_COLOR
    for message in messages:
        print(f"{color}{message}{reset_color}", **kwargs)


def print_and_return(obj, *args, **kwargs):
    print(obj, *args, **kwargs)
    return obj


def print_progress(value: int = None, total_value: int = None, step: int = 10):
    if value is None or step < 0:
        return
    str_total = f'/{total_value:,}' if total_value else ''
    len_total = max(len(str_total), 6)
    if value % (step * 100) == 0:
        print(f'+ {value:>{len_total},}{str_total} @ {time.strftime("%H:%M:%S")}', flush=True)
    elif value % (step * 50) == 0:
        print('+', end='', flush=True)
    elif value % (step * 10) == 0:
        print(':', end='', flush=True)
    elif value % step == 0:
        print('.', end='', flush=True)


class _ThreadColorFormatter(colorlog.ColoredFormatter):
    def format(self, record):
        record.msg = f"{_get_thread_color()}{record.msg}{_RESET_COLOR}"
        return super().format(record)


def flush_logger(logger):
    if not logger:
        return
    for handler in logger.handlers:
        handler.flush()


def get_colored_logger(name='root', level=logging.INFO):
    """Configure and return a logger with colored output."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)
        fmt = "%(log_color)s%(asctime)s %(levelname)s - [%(name)s] - %(message)s"
        formatter = _ThreadColorFormatter(fmt=fmt, reset=True)
        handler = colorlog.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


class Counter(dict[str, int]):
    def __init__(self, *args, **kwargs):
        super(Counter, self).__init__(*args, **kwargs)
        self.timestamp = time.time()
        self.last_progress_call = 0
        self.lock = threading.Lock()

    def __repr__(self):
        return self.to_str(60, 'Counter')

    def to_str(self, width=40, title=''):
        if not self:
            return ""
        if width < 23:
            width = 23

        v2str = lambda v: (f' {v:,.4f}' if v > 10 else f' {v:,.6f}').rstrip('0').rstrip('.')

        new_dict = {f'{k} ': v2str(v) for k, v in self.items()}

        max_k = max([len(k) for k in new_dict.keys()])
        max_v = max([len(v) for v in new_dict.values()])

        if max_k + max_v + 6 > width:
            width = max_k + max_v + 6

        kw = width - max_v - 4
        s = '\n'.join([f'+ {k:.<{kw}}{v:.>{max_v}} +' for k, v in sorted(new_dict.items())])
        title = '' if not title else title + ' '
        dt = title + time.strftime("%Y-%m-%d %H:%M:%S")
        et = 'Escaped: ' + sec2str_hms(time.time() - self.timestamp)
        return f"\n+ {dt:-^{width - 4}} +\n{s}\n+ {et:-^{width - 4}} +\n"

    def get(self, key: str, default: int = 0) -> int:
        """Get value for key, with a default of 0 if not found."""
        return super().get(key, default)

    def set(self, key: str, value: int = 0) -> int:
        with self.lock:
            self[key] = value
            return self[key]

    def inc(self, key: str, value: int = 1) -> int:
        with self.lock:
            self[key] = self.get(key, 0) + value
            return self[key]

    @deprecated('use inc() instead')
    def incr(self, key: str, value: int = 1) -> int:
        with self.lock:
            self[key] = self.get(key, 0) + value
            return self[key]

    @deprecated('use inc() instead')
    def increment(self, key: str, value: int = 1) -> int:
        with self.lock:
            self[key] = self.get(key, 0) + value
            return self[key]

    def reset(self):
        with self.lock:
            self.clear()
            self.timestamp = time.time()

    def log_progress(self, key: str = None, modulus: int = 1, interval: int = 300):
        if not self:
            return
        modulus = max(1, modulus) if modulus else 1
        has_key = key and key in self
        if (time.time() - self.last_progress_call) > interval:
            printc(self, flush=True)
            with self.lock:
                self.last_progress_call = time.time()
        elif (has_key and self.get(key, 0) % modulus == 0):
            printc(self, flush=True)
            with self.lock:
                self.last_progress_call = time.time()


if __name__ == "__main__":
    print_cmd()
    thread_names = [
        'main thread', 'thread-123', 'thread-123xxx', 'thread-sdf'

    ]
    for tn in thread_names:
        # remove all \D from x
        xx = ''.join(filter(str.isdigit, tn.split('-')[-1]))

        print(xx)

    c = Counter()
    for i in range(2000):
        c.inc('total')
        c.print_progress('total')
        time.sleep(0.001)
