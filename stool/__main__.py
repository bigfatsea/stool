from .misc_utils import *
from .logging_utils import *
from .date_utils import *
from concurrent.futures import ThreadPoolExecutor

# Your main script logic using the functions from the imported modules
if __name__ == '__main__':
    # do not touch the following line, git hook will update it automatically
    latest_commit_time = "2024-05-07 23:47:02"
    print(f'Latest commit time: {latest_commit_time}')


    print_cmd()

    counter = Counter()
    counter.to_str()
    counter.log_progress()
    counter.incr('x')
    counter.incr('xx' * 10, -10000.12300)
    counter.incr('xx' * 20, 100000001000.0000)
    counter.increment('y', 0.0001)
    counter.increment('z', 0.0030001)
    counter.increment('zz', 0.000000)
    counter.log_progress()

    xxx = logging.getLogger('xxx')
    xxx.error('This is a message from the xxx.')
    logger1 = get_colored_logger('worker')

    logger = get_colored_logger('worker')

    logger1.info('logger1')


    def worker():
        """Example worker function to log and print messages."""
        thread_name = threading.current_thread().name
        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        logger.critical("This is a critical message")
        time.sleep(1 + 0.1 * get_thread_number())
        printc(f"This is a message from the {thread_name}|{get_thread_number()} thread.")


    worker()
    time.sleep(0.5)
    logger.info('-' * 30)

    with ThreadPoolExecutor(max_workers=2) as executor:
        for i in range(2):
            executor.submit(worker)

    start = '2024-01-10'
    end = '2024-01-17'

    print('\n'.join([str(x) for x in generate_time_ranges(start, end)]))
    print('--')
    print('\n'.join([str(x) for x in generate_time_ranges(start, end, 'weekly')]))
    print('--')
    print('\n'.join([str(x) for x in generate_time_ranges(start, end, '5')]))
    print('--')
    print('\n'.join([str(x) for x in generate_time_ranges(start, end, 1)]))
    print('--')

    print('\n'.join([str(x) for x in split_into_months(start, end)]))
