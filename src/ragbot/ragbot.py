from dependency_injector.wiring import Provide, inject

from ragbot.container import RagbotContainer
from ragbot.interfaces import ChatService, LoggerFactoryService


@inject
async def run(
    *,
    logger_factory: LoggerFactoryService = Provide[RagbotContainer.logger_factory],
    chat_service: ChatService = Provide[RagbotContainer.chat_service],
) -> None:
    logger = logger_factory.get_logger("ragbot_runner")
    logger.info("Starting Ragbot...")

    try:
        async for chat_message in chat_service.messages():
            logger.info(f"Received message: {chat_message.message_text}")
            # TODO: Process the message here
            await chat_message.reply("Hello, world!")
    except Exception:
        logger.exception("Ragbot encountered an unexpected error!")
        raise
