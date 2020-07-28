import logging
import sys


def get_logger(log_name):
    logger = logging.getLogger(log_name)
    ch = logging.StreamHandler(sys.stdout)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger