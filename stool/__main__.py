from .misc_utils import *
from .logging_utils import *
from .date_utils import *
from concurrent.futures import ThreadPoolExecutor


# Your main script logic using the functions from the imported modules
if __name__ == '__main__':
    latest_commit_time = "2024-03-16 00:51:24"

    print(f'Latest commit time: {latest_commit_time}')

    counter = Counter()
    counter.log_progress()
    counter.incr('x')
    counter.log_progress()

    print_cmd()
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
    end = '2024-01-11'

    print('\n'.join([str(x) for x in generate_time_ranges(start, end)]))
    print('--')
    print('\n'.join([str(x) for x in generate_time_ranges(start, end, 'weekly')]))
    print('--')
    print('\n'.join([str(x) for x in generate_time_ranges(start, end, '5')]))
    print('--')
    print('--')

    print('\n'.join([str(x) for x in split_into_months(start, end)]))
