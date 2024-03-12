import logging
import threading
import colorlog
import time
import os
import sys

# Thread-specific colors
_THREAD_COLORS = [34, 36, 32, 33, 31, 35]

# convert seconds into hh:mm:ss
def sec2str(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}"

def get_thread_number():
    """Get the thread number."""
    thread_name = threading.current_thread().name
    return int(thread_name.split('-')[-1]) if '-' in thread_name else -1


def _get_thread_color():
    """Get color based on the thread number."""
    thread_number = get_thread_number()
    return 37 if thread_number < 0 else _THREAD_COLORS[thread_number % len(_THREAD_COLORS)]


def print_cmd():
    header = 'START @ ' + time.strftime("%Y-%m-%d %H:%M:%S")
    cmd = f"{os.path.basename(sys.argv[0])} {' '.join(sys.argv[1:])}"
    print(f"\n{header:-^80}\n {cmd}\n{'-' * 80}")


def printc(message):
    """Print colored message based on the thread number."""
    color = _get_thread_color()
    print(f"{color}{message}")


class _ThreadColorFormatter(colorlog.ColoredFormatter):
    def format(self, record):
        record.msg = f"{_get_thread_color()}{record.msg}"
        return super().format(record)


def get_colored_logger(name='root', level=logging.INFO):
    """Configure and return a logger with colored output."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)
        fmt = "%(log_color)s%(asctime)s %(levelname)s - [%(threadName)s] - %(message)s"
        formatter = _ThreadColorFormatter(fmt=fmt, reset=True)
        handler = colorlog.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


class Counter(dict):
    def __init__(self, *args, **kwargs):
        super(Counter, self).__init__(*args, **kwargs)
        self.timestamp = time.time()
        self.last_progress_call = 0
        self.lock = threading.Lock()

    def __repr__(self):
        return self.to_str(60, 'Counter')

    def to_str(self, width=40, title=''):
        if width < 23:
            width = 23
        max_k = max([len(k) for k in self.keys()])
        max_v = max([len(f'{v:,}') for v in self.values()])

        if max_k + max_v + 5 > width:
            width = max_k + max_v + 5

        kw = width - max_v - 4

        s = '\n'.join([f'+ {k:.<{kw}}{v:.>{max_v},} +' for k, v in sorted(self.items())])
        title = '' if not title else title + ' '
        dt = title + time.strftime("%Y-%m-%d %H:%M:%S")
        et = 'Escaped: ' + sec2str(time.time() - self.timestamp)
        return f"\n+ {dt:-^{width - 4}} +\n{s}\n+ {et:-^{width - 4}} +\n"

    def set(self, key, value=0):
        with self.lock:
            self[key] = value
            return self[key]

    def incr(self, key, value=1):
        with self.lock:
            self[key] = self.get(key, 0) + value
            return self[key]

    def reset(self):
        with self.lock:
            self.clear()
            self.timestamp = time.time()

    def log_progress(self, key=None, modulus=1, interval=300):
        if not self:
            return
        modulus = max(1, modulus) if modulus else 1
        has_key = key and key in self
        if (time.time() - self.last_progress_call) > interval:
            printc(self)
            with self.lock:
                self.last_progress_call = time.time()
        elif (has_key and self.get(key, 0) % modulus == 0):
            printc(self)
            with self.lock:
                self.last_progress_call = time.time()
