from dependency_injector.wiring import Provide, inject

from ragbot.container import RagbotContainer
from ragbot.interfaces import LoggerFactoryService


@inject
async def run(
    *,
    logger_factory: LoggerFactoryService = Provide[RagbotContainer.logger_factory],
) -> None:
    logger = logger_factory.get_logger("ragbot_runner")

    logger.info("Starting Ragbot...")

    try:
        pass
        # TODO: Implement the bot logic here.
    except Exception:
        logger.exception("Ragbot encountered an unexpected error!")
        raise
