from dependency_injector import containers, providers
from openai import AsyncClient
from pymilvus import AsyncMilvusClient

from ragbot.config import RagbotConfig
from ragbot.interfaces import AiChatService, ChatService, LoggerFactoryService
from ragbot.services import LoggerFactory, OpenAIChatService, RagbotDiscordChat


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
    )

    milvus_client: providers.Singleton[AsyncMilvusClient] = providers.Singleton(
        AsyncMilvusClient,
        uri=config.milvus.uri,
    )
