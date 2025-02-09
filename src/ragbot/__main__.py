import asyncio

from ragbot import ragbot
from ragbot.config import RagbotConfig
from ragbot.container import RagbotContainer


def bootstrap_app() -> None:
    # Initialize the DI container:
    container = RagbotContainer()

    # Load the configuration:
    config = RagbotConfig()
    container.config.from_pydantic(config)

    logger = container.logger_factory().get_logger("ragbot_setup")
    logger.info("Bootsrapping Ragbot...")

    # Inject the dependencies into existing objects and functions:
    logger.debug("Wiring up the DI container...")
    container.wire(
        packages=[
            "ragbot",
        ]
    )

    logger.info("Ragbot bootstrapped successfully!")


def main() -> None:
    bootstrap_app()
    asyncio.run(ragbot.run())


if __name__ == "__main__":
    main()
