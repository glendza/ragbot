from logging import Logger

import aiohttp

from ragbot.interfaces import EmbeddingService


class JinaEmbeddingService(EmbeddingService):
    def __init__(
        self,
        logger: Logger,
        api_key: str,
        api_endpoint: str,
    ) -> None:
        self._logger = logger
        self._api_key = api_key
        self._api_endpoint = api_endpoint

    async def create_embeddings(self, *input: str) -> list[list[float]]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }

        data = {
            "input": input,
            "model": "jina-embeddings-v3",
            "task": "retrieval.passage",
            "normalized": True,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self._api_endpoint,
                headers=headers,
                json=data,
            ) as response:
                response.raise_for_status()
                json = await response.json()

                self._logger.debug(f"Jina Embedding Responses: {json}")

                return [embedding["embedding"] for embedding in json["data"]]
