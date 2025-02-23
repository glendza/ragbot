from abc import ABC, abstractmethod


class IRCClient(ABC):
    @abstractmethod
    async def send_message_to_channel(self, channel: str, message: str) -> None:
        """
        Send a message to a channel.
        """
        pass

    @abstractmethod
    async def send_private_message(self, recipient: str, message: str) -> None:
        """
        Send a private message to a user.
        """
        pass
