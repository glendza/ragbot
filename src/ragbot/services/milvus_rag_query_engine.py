from logging import Logger

from pymilvus import AsyncMilvusClient

from ragbot.interfaces import EmbeddingService, RagQueryEngine
from ragbot.models.dtos import RagSearchResults

VECTOR_FIELD_NAME = "vector"
OUTPUT_FIELD_NAME = "content"


class MilvusRagQueryEngine(RagQueryEngine):
    def __init__(
        self,
        *,
        collection_name: str,
        max_results: int,
        logger: Logger,
        milvus_client: AsyncMilvusClient,
        embedding_service: EmbeddingService,
    ):
        self._collection_name = collection_name
        self._max_results = max_results
        self._logger = logger
        self._milvus_client = milvus_client
        self._embedding_service = embedding_service

    async def process_query(self, query: str) -> RagSearchResults:
        self._logger.info(f"Processing query: {query}")

        # Get the embeddings for the query:
        query_embedding = await self._embedding_service.create_embeddings(query)

        # Search for similar vectors in Milvus:
        results = (
            await self._milvus_client.search(
                collection_name=self._collection_name,
                data=query_embedding,
                anns_field=VECTOR_FIELD_NAME,
                limit=self._max_results,
                output_fields=[OUTPUT_FIELD_NAME],
                search_params={
                    "metric_type": "COSINE",  # Cosine similarity (higher is more similar)
                    "params": {
                        "nprobe": 10,
                    },
                },
            )
        )[0]  # Since we send only one query vector, we will always have only one result.

        self._logger.info(f"Found {len(results)} results.")

        return RagSearchResults.model_validate(
            [{"id": r["id"], "distance": r["distance"], "content": r["entity"]["content"]} for r in results]
        )
