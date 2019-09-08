import signal
from contextlib import contextmanager


@contextmanager
def timeout(time):
    signal.signal(signal.SIGALRM, raise_timeout)
    signal.alarm(time)

    try:
        yield
    except TimeoutError:
        pass
    finally:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def raise_timeout(signum, frame):
    raise TimeoutError


def my_func():
    # Add a timeout block.
    with timeout(1):
        print('entering block')
        import time
        time.sleep(10)
        print('This should never get printed because the line before timed out')
