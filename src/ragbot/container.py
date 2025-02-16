from dependency_injector import containers, providers
from openai import AsyncClient

from ragbot.interfaces import AiChatService, ChatService, LoggerFactoryService
from ragbot.services import LoggerFactory, OpenAIChatService, RagbotDiscordChat


class RagbotContainer(containers.DeclarativeContainer):
    """
    DI container for configuring services and their lifecycles.
    """

    config = providers.Configuration()

    logger_factory: providers.Singleton[LoggerFactoryService] = providers.Singleton(
        LoggerFactory,
        log_level=config.log_level,
    )

    chat_service: providers.Singleton[ChatService] = providers.Singleton(
        RagbotDiscordChat,
        token=config.discord.token,
    )

    openai: providers.Singleton[AsyncClient] = providers.Singleton(
        AsyncClient,
        api_key=config.openai.api_key,
    )

    ai_chat_service: providers.Factory[AiChatService] = providers.Factory(
        OpenAIChatService,
        openai_client=openai,
    )
