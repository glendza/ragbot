import re

from .models import ChannelMessage, PrivateMessage, UnclassifiedMessage

CHANNEL_MESSAGE_PATTERN = re.compile(r"^:(?P<hostmask>\S+) PRIVMSG (?P<channel>#\S+) :(?P<message>.+)\r\n$")
PRIVATE_MESSAGE_PATTERN = re.compile(r"^:(?P<hostmask>\S+) PRIVMSG (?P<recipient>\S+) :(?P<message>.+)\r\n$")


def is_system_message(message: str) -> bool:
    return message.startswith(":")


def is_connection_success_message(message: str) -> tuple[bool, str | None]:
    parts = message.split()
    if parts[1] in ["001", "376", "422"]:
        server_name = parts[0][1:]
        return True, server_name
    return False, None


def get_pong_message(message: str) -> str | None:
    if message.startswith("PING"):
        return f"PONG {message.split()[1]}"
    return None


def format_channel_name(channel: str) -> str:
    if channel.startswith("#"):
        return channel
    return "#" + channel


def get_user_from_hostmask(hostmask: str) -> str:
    return hostmask.split("!")[0]


def is_tagged_message(
    message: ChannelMessage,
    bot_nickname: str,
) -> bool:
    return f"@{bot_nickname}" in message.message


def parse_message(full_message: str) -> ChannelMessage | PrivateMessage | UnclassifiedMessage:
    """
    Parse a message from the IRC server.
    """
    # Handle channel messages:
    match = re.match(CHANNEL_MESSAGE_PATTERN, full_message)
    if match:
        return ChannelMessage(
            sender=get_user_from_hostmask(match.group("hostmask")),
            hostmask=match.group("hostmask"),
            channel=match.group("channel"),
            message=match.group("message"),
        )

    # Handle private messages:
    if match := re.match(PRIVATE_MESSAGE_PATTERN, full_message):
        return PrivateMessage(
            sender=get_user_from_hostmask(match.group("hostmask")),
            hostmask=match.group("hostmask"),
            recipient=match.group("recipient"),
            message=match.group("message"),
        )

    # Handle channel messages:
    return UnclassifiedMessage(message=full_message)
