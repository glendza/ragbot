import asyncio
from logging import Logger
from typing import AsyncGenerator

from ragbot.interfaces import ChatService

from . import utils as chat_utils
from .interfaces import IRCClient
from .message import IRCMessage
from .models import ChannelMessage, PrivateMessage


class RagbotIRCChat(ChatService, IRCClient):
    def __init__(
        self,
        *,
        logger: Logger,
        host: str,
        port: int,
        nickname: str,
        channels: list[str],
    ):
        self._logger = logger
        self._host = host
        self._port = port
        self._nickname = nickname
        self._channels = [chat_utils.format_channel_name(channel) for channel in channels]

        # Initialize reader and writer:
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None

        # Initialize events and queues:
        self._connected = asyncio.Event()
        self._message_queues: list[asyncio.Queue[IRCMessage]] = []
        self._queue_lock: asyncio.Lock = asyncio.Lock()

    async def messages(self) -> AsyncGenerator[IRCMessage, None]:
        # Start the bot if not already running:
        await self._start_bot_if_not_running()

        message_queue: asyncio.Queue[IRCMessage] = asyncio.Queue()

        try:
            async with self._queue_lock:
                self._message_queues.append(message_queue)
            while True:
                message = await message_queue.get()
                self._logger.debug("Yielding message: %s", message.message_text)
                yield message
                message_queue.task_done()
                self._logger.debug("Message processed: %s", message.message_text)
                await asyncio.sleep(0.1)
        finally:
            async with self._queue_lock:
                self._message_queues.remove(message_queue)

                if len(self._message_queues) == 0:
                    await self._stop_bot()

    async def send_message_to_channel(self, channel: str, message: str) -> None:
        """
        Send a message to a channel.
        """
        await self._write(f"PRIVMSG {channel} :{message}")

    async def send_private_message(self, recipient: str, message: str) -> None:
        """
        Send a private message to a user.
        """
        await self._write(f"PRIVMSG {recipient} :{message}")

    async def _start_bot_if_not_running(self) -> None:
        """
        Connect to the IRC server.
        """
        if self._reader and self._writer:
            self._logger.warning("Already connected to the server")
            return

        self._logger.info(f"Connecting to {self._host} on port {self._port}...")
        self._reader, self._writer = await asyncio.open_connection(self._host, self._port)

        # Start the message loop:
        asyncio.create_task(self._listen_to_messages())

        # Log in to the server:
        self._logger.info("Logging in as %s", self._nickname)
        await self._write(
            f"NICK {self._nickname}",
            f"USER {self._nickname} 0 * :{self._nickname}",
        )

        # Wait for the connection to be established:
        await self._connected.wait()

        # Join the channels:
        for channel in self._channels:
            await self._join_channel(channel)

    async def _stop_bot(self) -> None:
        """
        Close the connection to the server.
        """
        if self._writer:
            self._writer.close()
            await self._writer.wait_closed()
            self._reader = None
            self._writer = None
            self._logger.info("Disconnected from the server")

    async def _write(self, *messages: str) -> None:
        """
        Write a message to the server.
        """
        if not self._writer:
            raise ConnectionError("Not connected to the server")

        for message in messages:
            self._writer.write(f"{message}\r\n".encode())

        await self._writer.drain()

    async def _join_channel(self, channel: str) -> None:
        """
        Join a channel on the server.
        """
        await self._write(f"JOIN {channel}")
        self._logger.info(f"Joined channel: {channel}")

    def _get_outgoing_message(self, message: str) -> IRCMessage | None:
        parsed_message = chat_utils.parse_message(message)

        if isinstance(parsed_message, ChannelMessage) and chat_utils.is_tagged_message(
            message=parsed_message,
            bot_nickname=self._nickname,
        ):
            return IRCMessage(
                client=self,
                message=parsed_message,
            )

        if isinstance(parsed_message, PrivateMessage):
            return IRCMessage(
                client=self,
                message=parsed_message,
            )

        return None

    async def _listen_to_messages(self) -> None:
        """
        Listen to incoming messages and respond accordingly.
        """
        while self._reader:
            data = await self._reader.read(1024)
            if data:
                message = data.decode("utf-8")
                self._logger.debug(f"Received: {message}")

                if chat_utils.is_system_message(message):
                    is_connection_success, server_name = chat_utils.is_connection_success_message(message)
                    if is_connection_success:
                        self._logger.info(f"Connected to server: {server_name}")
                        self._connected.set()

                # Respond to PING from the server to keep the connection alive:
                if pong_message := chat_utils.get_pong_message(message):
                    await self._write(pong_message)

                # All the other messages are to be sent to the consumers:
                outgoing_message = self._get_outgoing_message(message)
                if not outgoing_message:
                    continue
                async with self._queue_lock:
                    await asyncio.gather(*(queue.put(outgoing_message) for queue in self._message_queues))
