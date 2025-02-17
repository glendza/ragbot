from abc import ABC, abstractmethod
from typing import Awaitable


class EmbeddingService(ABC):
    @abstractmethod
    def create_embeddings(self, *input: str) -> Awaitable[list[list[float]]]:
        pass
