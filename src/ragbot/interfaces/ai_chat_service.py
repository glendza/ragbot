from abc import ABC, abstractmethod
from typing import Awaitable


class AiChatService(ABC):
    @abstractmethod
    def process_message(self, message: str) -> Awaitable[str]: ...
