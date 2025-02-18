from abc import ABC, abstractmethod
from typing import Awaitable

from ragbot.models.dtos import RagSearchResults
from ragbot.models.structured_outputs import ChatResponse


class AiChatService(ABC):
    @abstractmethod
    def process_message(
        self,
        *,
        message: str,
        retrieved_context: RagSearchResults,
        summarized_chat_history: str | None,
    ) -> Awaitable[ChatResponse]: ...
