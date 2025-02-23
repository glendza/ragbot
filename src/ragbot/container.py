import importlib
import typing

from dependency_injector import containers, providers
from pymilvus import AsyncMilvusClient
from tinydb import TinyDB

from ragbot.config import RagbotConfig
from ragbot.interfaces import (
    AIChatService,
    ChatService,
    ContextStorageService,
    DomainProvider,
    EmbeddingService,
    LoggerFactoryService,
    RagQueryEngine,
)
from ragbot.services import LoggerFactory, MilvusRagQueryEngine, TinydbContextStorage

if typing.TYPE_CHECKING:
    from openai import AsyncClient


def init_domain(module_path: str) -> DomainProvider:
    return typing.cast(
        DomainProvider,
        importlib.import_module(module_path),
    )


class RagbotContainer(containers.DeclarativeContainer):
    """
    DI container for configuring services and their lifecycles.
    """

    @classmethod
    def from_default_config(cls) -> "RagbotContainer":
        """
        Create a new container instance with the default configuration.
        """
        config = RagbotConfig()
        c = cls()

        # Providing backend for Chat Service:
        if config.chat_backend == "discord" and config.discord:
            c.chat_service.override(
                providers.Singleton(
                    "ragbot.backends.chat_clients.discord_client.RagbotDiscordChat",
                    logger=providers.Singleton(
                        lambda lf: lf.get_logger("discord_chat"),
                        lf=c.logger_factory,
                    ),
                    token=config.discord.token,
                )
            )
        elif config.chat_backend == "irc" and config.irc:
            c.chat_service.override(
                providers.Singleton(
                    "ragbot.backends.chat_clients.irc_client.RagbotIRCChat",
                    logger=providers.Singleton(
                        lambda lf: lf.get_logger("irc_chat"),
                        lf=c.logger_factory,
                    ),
                    host=config.irc.host,
                    port=config.irc.port,
                    nickname=config.irc.nickname,
                    channels=config.irc.channels,
                )
            )

        # Providing backend for AI Chat Service:
        if config.ai_chat_backend == "openai" and config.openai:
            c.ai_chat_service.override(
                providers.Factory(
                    provides="ragbot.backends.ai_chat_providers.openai_chat_service.OpenAIChatService",
                    logger=providers.Factory(
                        lambda lf: lf.get_logger("openai_chat_service"),
                        lf=c.logger_factory,
                    ),
                    openai_client=c.openai_async_client,
                    model=config.openai.model,
                    temperature=config.openai.temperature,
                    max_tokens=config.openai.max_tokens,
                    conversational_schema=providers.Callable(
                        provides=lambda d: d.get_conversational_schema(),
                        d=c.domain,
                    ),
                )
            )
        elif config.ai_chat_backend == "mistralai" and config.mistralai:
            c.ai_chat_service.override(
                providers.Factory(
                    provides="ragbot.backends.ai_chat_providers.mistralai_chat_service.MistralAIChatService",
                    logger=providers.Factory(
                        lambda lf: lf.get_logger("mistralai_chat_service"),
                        lf=c.logger_factory,
                    ),
                    mistralai_client=providers.Singleton(
                        "mistralai.Mistral",
                        api_key=config.mistralai.api_key,
                    ),
                    model=config.mistralai.model,
                    temperature=config.mistralai.temperature,
                    max_tokens=config.mistralai.max_tokens,
                    conversational_schema=providers.Callable(
                        provides=lambda d: d.get_conversational_schema(),
                        d=c.domain,
                    ),
                )
            )

        # Providing backend for Embedding Service:
        if config.embeddings_backend == "jina" and config.jina:
            c.embedding_service.override(
                providers.Factory(
                    provides="ragbot.backends.embedding_providers.jina_embedding_service.JinaEmbeddingService",
                    logger=providers.Factory(
                        lambda lf: lf.get_logger("jina_embedding_service"),
                        lf=c.logger_factory,
                    ),
                    api_key=config.jina.api_key,
                    api_endpoint=config.jina.api_endpoint,
                )
            )
        elif config.embeddings_backend == "openai" and config.openai:
            c.embedding_service.override(
                providers.Factory(
                    provides="ragbot.backends.embedding_providers.openai_embedding_service.OpenAIEmbeddingService",
                    logger=providers.Factory(
                        lambda lf: lf.get_logger("openai_embedding_service"),
                        lf=c.logger_factory,
                    ),
                    openai_client=c.openai_async_client,
                    embedding_model=config.openai.embedding_model,
                )
            )

        c.config.from_pydantic(config)
        return c

    config = providers.Configuration()

    logger_factory: providers.Singleton[LoggerFactoryService] = providers.Singleton(
        LoggerFactory,
        log_level=config.log_level,
    )

    domain: providers.Resource[DomainProvider] = providers.Resource(
        init_domain,
        module_path=config.domain_module_path,
    )

    chat_service: providers.AbstractSingleton[ChatService] = providers.AbstractSingleton()

    openai_async_client: providers.Singleton["AsyncClient"] = providers.Singleton(
        "openai.AsyncClient",
        api_key=config.openai.api_key,
    )

    ai_chat_service: providers.AbstractFactory[AIChatService] = providers.AbstractFactory()

    milvus_client: providers.Singleton[AsyncMilvusClient] = providers.Singleton(
        AsyncMilvusClient,
        uri=config.milvus.uri,
    )

    embedding_service: providers.Factory[EmbeddingService] = providers.AbstractFactory()

    rag_query_engine: providers.Factory[RagQueryEngine] = providers.Factory(
        MilvusRagQueryEngine,
        collection_name=config.milvus.collection_name,
        max_results=config.rag_retrieval_limit,
        logger=providers.Factory(
            lambda lf: lf.get_logger("rag_query_engine"),
            lf=logger_factory,
        ),
        milvus_client=milvus_client,
        embedding_service=embedding_service,
    )

    tinydb = providers.Singleton(  # Singleton because of the concurrency issues with TinyDB
        TinyDB,
        path=config.tinydb.db_path,
    )

    context_storage: providers.Factory[ContextStorageService] = providers.Factory(
        TinydbContextStorage,
        db=tinydb,
        table_name=config.tinydb.table_name,
        logger=providers.Factory(
            lambda lf: lf.get_logger("tinydb_context_storage"),
            lf=logger_factory,
        ),
    )
