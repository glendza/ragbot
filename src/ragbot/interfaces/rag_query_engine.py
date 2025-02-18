from abc import ABC, abstractmethod

from ragbot.models.dtos import RagSearchResults


class RagQueryEngine(ABC):
    @abstractmethod
    async def process_query(self, query: str) -> RagSearchResults: ...
