# logging_config.py
import logging

def setup_logging(debug_mode='DEBUG'):
    """
    Two Logger Instances: This script creates two separate logger objects, logger_game and logger_info, each with their own file handlers pointing to different log files. The logger_game object is used for general debugging and logging, while logger_info is used for specific analytics logging. The logger_game object is set to log messages of level DEBUG and above, while logger_info is set to log messages of level INFO and above. The logger_game object also has a console handler that logs messages of level CRITICAL and above. The console handler is commented out by default, but can be enabled by uncommenting the line that sets its level to DEBUG. The logger_info object has a file handler that logs messages of level INFO and above. Both logger objects are set to not propagate their messages to the root logger.
    """

    # the basic debugging logger
    logger = logging.getLogger('poker_game')
    logger.setLevel(logging.DEBUG)  # Adjust this to the desired minimum level across handlers

    # File handler
    f_handler = logging.FileHandler('logs/poker_game_info.log')
    f_handler.setLevel(logging.INFO)

    f_format = logging.Formatter('%(message)s')
    # f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)

    # Console handler
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.CRITICAL)
    
    #########################################################
    # set the level of logging in the tests for convenience #
    #########################################################

    if debug_mode == 'DEBUG':
        c_handler.setLevel(logging.DEBUG)
        f_handler.setLevel(logging.INFO)
    elif debug_mode == 'INFO':
        c_handler.setLevel(logging.CRITICAL)
        f_handler.setLevel(logging.INFO)
    elif debug_mode == 'CRITICAL':
        c_handler.setLevel(logging.CRITICAL)
        f_handler.setLevel(logging.CRITICAL)

    c_format = logging.Formatter('%(name)s - %(message)s')
    c_handler.setFormatter(c_format)
    logger.addHandler(c_handler)

    # Logger for specific info logging
    logger_info = logging.getLogger('poker_game_analytics')
    logger_info.setLevel(logging.INFO)  # This logger will handle only INFO level specifics

    f_handler_info = logging.FileHandler('logs/poker_game_analytics.log')
    f_handler_info.setLevel(logging.INFO)
    f_format_info = logging.Formatter('%(asctime)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    f_handler_info.setFormatter(f_format_info)
    logger_info.addHandler(f_handler_info)

    # Prevent logging from propagating to the root logger
    logger.propagate = False
    logger_info.propagate = False

    return logger
