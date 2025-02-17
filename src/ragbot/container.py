import importlib
import typing

from dependency_injector import containers, providers
from openai import AsyncClient
from pymilvus import AsyncMilvusClient

from ragbot.config import RagbotConfig
from ragbot.interfaces import AiChatService, ChatService, DomainProvider, LoggerFactoryService
from ragbot.services import LoggerFactory, OpenAIChatService, OpenAIEmbeddingService, RagbotDiscordChat


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
        c = cls()
        c.config.from_pydantic(RagbotConfig())
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

    chat_service: providers.Singleton[ChatService] = providers.Singleton(
        RagbotDiscordChat,
        token=config.discord.token,
    )

    openai: providers.Factory[AsyncClient] = providers.Factory(
        AsyncClient,
        api_key=config.openai.api_key,
    )

    ai_chat_service: providers.Factory[AiChatService] = providers.Factory(
        OpenAIChatService,
        openai_client=openai,
        conversational_schema=providers.Callable(
            lambda d: d.get_conversational_schema(),
            d=domain,
        ),
    )

    milvus_client: providers.Singleton[AsyncMilvusClient] = providers.Singleton(
        AsyncMilvusClient,
        uri=config.milvus.uri,
    )

    embedding_service: providers.Factory[OpenAIEmbeddingService] = providers.Factory(
        OpenAIEmbeddingService,
        openai_client=openai,
        embedding_model=config.openai.embedding_model,
    )
