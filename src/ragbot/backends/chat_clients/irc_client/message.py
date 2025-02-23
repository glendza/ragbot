import asyncio

from ragbot.interfaces import ChatMessage

from .interfaces import IRCClient
from .models import ChannelMessage, PrivateMessage


class IRCMessage(ChatMessage):
    def __init__(
        self,
        *,
        client: IRCClient,
        message: ChannelMessage | PrivateMessage,
    ) -> None:
        self._client = client
        self._message = message

        self._has_replied = False
        self._lock = asyncio.Lock()

    @property
    def message_text(self) -> str:
        return self._message.message

    @property
    def thread_id(self) -> str:
        return self._message.hostmask

    async def reply(self, message: str) -> None:
        async with self._lock:
            if self._has_replied:
                raise RuntimeError("Message has already been replied to!")

            if isinstance(self._message, ChannelMessage):
                await self._client.send_message_to_channel(
                    channel=self._message.channel,
                    message=message,
                )
            elif isinstance(self._message, PrivateMessage):
                await self._client.send_private_message(
                    recipient=self._message.sender,
                    message=message,
                )
            else:
                raise ValueError("Unknown message type!")

            self._has_replied = True
