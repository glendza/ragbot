from dependency_injector import containers, providers

from ragbot.interfaces import ChatService, LoggerFactoryService
from ragbot.services import LoggerFactory, RagbotDiscordChat


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
