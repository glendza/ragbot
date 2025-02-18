import asyncio

import discord

from ragbot.interfaces import ChatMessage

from . import utils as discord_utils


class DiscordMessage(ChatMessage):
    def __init__(
        self,
        *,
        thread: discord.Thread,
        message: discord.Message,
        context: str | None = None,
    ) -> None:
        self._thread = thread
        self._message = message
        self._context = context

        self._has_replied = False
        self._lock = asyncio.Lock()

    @property
    def message_text(self) -> str:
        return self._message.content

    @property
    def thread_id(self) -> str:
        return str(self._thread.id)

    async def reply(self, message: str) -> None:
        async with self._lock:
            if self._has_replied:
                raise RuntimeError("Message has already been replied to!")

            await self._thread.send(message)
            # TODO: Log replies
            self._has_replied = True

            # When the message has been replied to, unlock the thread, and allow other bots/users to reply:
            await self._unlock_thread()

    async def lock_thread(self) -> None:
        await discord_utils.lock_thread(self._thread)

    async def _unlock_thread(self) -> None:
        await discord_utils.unlock_thread(self._thread)
