import asyncio
import logging
import typing

import discord

from ragbot.interfaces import ChatService

from . import utils as discord_utils
from .message import DiscordMessage

logger = logging.getLogger(__name__)


class RagbotDiscordChat(discord.Client, ChatService):
    def __init__(self, *, token: str) -> None:
        # Save the token:
        self._token = token

        # Whether the client has been initialized:
        self._bot_run_task: asyncio.Task[None] | None = None
        self._init_lock = asyncio.Lock()

        # Create a queue to store incoming messages:
        self._message_queues: list[asyncio.Queue[DiscordMessage]] = []
        self._queue_lock = asyncio.Lock()

        # Enable the necessary intents:
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        intents.guilds = True
        intents.emojis = True
        intents.guild_messages = True

        super().__init__(intents=intents)

    async def on_ready(self) -> None:
        logger.info(f"Logged in as {self.user}")

    async def on_message(self, message: discord.Message) -> None:
        # Avoid replying to ourselves:
        if message.author == self.user:
            return

        logger.debug(f"Received message: {message.content}")

        thread = await discord_utils.get_or_create_bot_thread(
            message=message,
            name="New Thread",
        )

        if thread:
            logger.info(f"Received message in thread: {thread.name}")

            outging_message = DiscordMessage(
                thread=thread,
                message=message,
            )

            # Lock the thread to prevent other bots/users from replying until the message is processed:
            await outging_message.lock_thread()

            # Forward the message to all the subscribers:
            async with self._queue_lock:
                logger.debug("Forwarding message to %d subscribers...", len(self._message_queues))
                for queue in self._message_queues:
                    await queue.put(outging_message)

    async def messages(self) -> typing.AsyncGenerator[DiscordMessage, None]:
        # Start the bot if it's not already running:
        await self._start_bot_if_not_running()

        # Create a new message queue:
        message_queue = asyncio.Queue[DiscordMessage]()

        # Add the message queue to the list of queues:
        async with self._queue_lock:
            self._message_queues.append(message_queue)
            logger.debug("Subscribed to messages from %d queues", len(self._message_queues))

        # Yield messages from the queue:
        try:
            while True:
                message = await message_queue.get()
                logger.debug("Yielding message: %s", message.message_text)
                yield message
                message_queue.task_done()
                logger.debug("Message processed: %s", message.message_text)
        finally:
            async with self._queue_lock:
                self._message_queues.remove(message_queue)

                if len(self._message_queues) == 0:
                    await self._stop_bot()

    async def _start_bot_if_not_running(self) -> None:
        async with self._init_lock:
            if not self._bot_run_task:
                logger.info("Starting the Discord bot...")
                self._bot_run_task = asyncio.create_task(self.start(self._token))
                logger.info("Discord bot started!")

    async def _stop_bot(self) -> None:
        await self.close()
        async with self._init_lock:
            if self._bot_run_task:
                self._bot_run_task.cancel()
                self._bot_run_task = None
        logger.info("Discord bot stopped!")
