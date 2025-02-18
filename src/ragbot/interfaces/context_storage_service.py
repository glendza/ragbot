import typing
from abc import ABC, abstractmethod


class ContextStorageService(ABC):
    @abstractmethod
    def store_message_data(
        self,
        *,
        thread_id: str,
        message: str,
        updated_context: str | None,
    ) -> typing.Awaitable[None]: ...

    @abstractmethod
    def retrieve_latest_summarized_history(self, *, thread_id: str) -> typing.Awaitable[str | None]: ...
