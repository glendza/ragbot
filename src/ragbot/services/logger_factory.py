import logging

from ragbot.interfaces import LoggerFactoryService
from ragbot.types.logging import LogLevel

LOG_FORMAT = "%(asctime)s %(levelname)-8s logger: %(name)-20s module: %(module)-20s message: %(message)s (line %(lineno)d, in %(funcName)s)"


class LoggerFactory(LoggerFactoryService):
    def __init__(self, *, log_level: LogLevel) -> None:
        self._configure_logging(log_level)

    def get_logger(self, name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        return logger

    def _configure_logging(self, log_level: LogLevel) -> None:
        logging.basicConfig(
            level=log_level,
            format=LOG_FORMAT,
        )
