import asyncio
from logging import Logger

import openai

from ragbot.interfaces import EmbeddingService


class OpenAIEmbeddingService(EmbeddingService):
    def __init__(
        self,
        logger: Logger,
        openai_client: openai.AsyncClient,
        embedding_model: str,
    ) -> None:
        self._logger = logger
        self._openai_client = openai_client
        self._embedding_model = embedding_model

    async def create_embeddings(self, *input: str) -> list[list[float]]:
        responses = await asyncio.gather(
            *[
                self._openai_client.embeddings.create(
                    model=self._embedding_model,
                    input=entry,
                )
                for entry in input
            ]
        )

        self._logger.debug(f"OpenAI Embedding Responses: {responses}")

        return [response.data[0].embedding for response in responses]
