import asyncio

import openai

from ragbot.interfaces import EmbeddingService


class OpenAIEmbeddingService(EmbeddingService):
    def __init__(
        self,
        openai_client: openai.AsyncClient,
        embedding_model: str,
    ) -> None:
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
        return [response.data[0].embedding for response in responses]
