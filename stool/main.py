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
