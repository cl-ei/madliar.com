import os

from etc.config import LOG_PATH

__all__ = ("logging", )


def __make_logger(name, log_file_name, level="DEBUG", log_format=None):
    import logging

    level_names = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARN': logging.WARNING,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'NOTSET': logging.NOTSET,
    }

    fh = logging.FileHandler(os.path.join(LOG_PATH, log_file_name))

    if log_format is None:
        log_format = '%(levelname)s %(asctime)s %(filename)s:%(lineno)d:%(funcName)s %(message)s'
    fh.setFormatter(logging.Formatter(log_format))

    logger = logging.getLogger(name)
    logger.setLevel(level_names.get(level.upper(), logging.DEBUG))
    logger.addHandler(fh)
    return logger


logging = __make_logger(
    name="madliar_app",
    log_file_name="madliar_app.log",
)
