import logging
from abc import ABC, abstractmethod


class LoggerFactoryService(ABC):
    @abstractmethod
    def get_logger(self, name: str) -> logging.Logger:
        pass
