import signal
import logging

# Retrieve the already configured logger
logger = logging.getLogger('poker_game')

# Define the exception to raise on timeout
class TimeoutException(Exception):
    pass

# Handler function to call when signal alarm triggers
def signal_handler(signum, frame):
    logger.info("Timeout reached")
    1/0
    raise TimeoutException("Function execution exceeded the allowed time limit")

# Decorator to apply timeout to functions for testing a lot of random games
def timeout(seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Set the signal handler
            signal.signal(signal.SIGALRM, signal_handler)
            # Schedule the alarm
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                # Cancel the alarm
                signal.alarm(0)
            return result
        return wrapper
    return decorator
