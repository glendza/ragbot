from abc import ABC, abstractmethod
from typing import Awaitable

from ragbot.models.dtos import RagSearchResults


class AiChatService(ABC):
    @abstractmethod
    def process_message(self, *, message: str, retrieved_context: RagSearchResults) -> Awaitable[str]: ...
