import asyncio

import torch
from sentence_transformers import SentenceTransformer

from ragbot.interfaces import EmbeddingService


class SentenceEmbedderService(EmbeddingService):
    def __init__(
        self,
        embedding_model: str,
    ) -> None:
        # initialize the embedding model:
        torch.cuda.empty_cache()
        self._model = SentenceTransformer(embedding_model)

    async def create_embeddings(self, *input: str) -> list[list[float]]:
        return await asyncio.to_thread(self._create_embeddings_sync, list(input))

    def _create_embeddings_sync(self, text_chunks: list[str]) -> list[list[float]]:
        # Generate embeddings for each text chunk:
        embeddings = self._model.encode(text_chunks, convert_to_numpy=True).tolist()
        return embeddings
