from misc_utils import *
from logging_utils import *
from date_utils import *

# Your main script logic using the functions from the imported modules
if __name__ == '__main__':
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