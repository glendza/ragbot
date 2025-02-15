import typing
from abc import ABC, abstractmethod


class ChatMessage(ABC):
    @property
    @abstractmethod
    def message_text(self) -> str:
        pass

    @abstractmethod
    def reply(self, message: str) -> typing.Awaitable[None]:
        pass


class ChatService(ABC):
    @abstractmethod
    def messages(self) -> typing.AsyncGenerator[ChatMessage, None]:
        pass
