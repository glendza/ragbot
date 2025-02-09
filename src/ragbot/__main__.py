import asyncio


def bootstrap_app() -> None:
    # TODO: Read configuration, setup logging, set up DI providers etc.
    pass


async def run_app() -> None:
    # TODO: Start the bot
    pass


def main() -> None:
    bootstrap_app()
    asyncio.run(run_app())


if __name__ == "__main__":
    main()
