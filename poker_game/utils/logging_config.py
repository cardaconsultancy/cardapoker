# logging_config.py
import logging

def setup_logging():
    logger = logging.getLogger('poker_game')
    logger.setLevel(logging.DEBUG)  # Adjust this to the desired minimum level across handlers

    # File handler
    f_handler = logging.FileHandler('poker_game.log')
    f_handler.setLevel(logging.INFO)
    f_format = logging.Formatter('%(message)s')
    # f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)

    # Console handler
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)
    c_format = logging.Formatter('%(name)s - %(message)s')
    c_handler.setFormatter(c_format)
    logger.addHandler(c_handler)

    # Prevent logging from propagating to the root logger
    logger.propagate = False

    return logger
