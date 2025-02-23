import discord


def get_bot_user_from_message(guild: discord.Message) -> discord.Member | None:
    if not guild.guild:
        return None

    return guild.guild.me


def get_thread_from_message(message: discord.Message) -> discord.Thread | None:
    if not message.channel:
        return None

    if message.channel.type != discord.ChannelType.public_thread:
        return None

    if not isinstance(message.channel, discord.Thread):
        return None

    if not isinstance(message.channel.owner, discord.Member):
        return None

    if not message.guild:
        return None

    return message.channel


async def get_or_create_bot_thread(
    *,
    message: discord.Message,
    name: str,
) -> discord.Thread | None:
    bot_user = get_bot_user_from_message(message)
    if not bot_user:
        return None

    thread = get_thread_from_message(message)
    if thread and thread.owner == bot_user:
        return thread

    if bot_user.mentioned_in(message):
        return await message.create_thread(name=name)

    return None


async def lock_thread(thread: discord.Thread) -> None:
    await thread.edit(locked=True)


async def unlock_thread(thread: discord.Thread) -> None:
    await thread.edit(locked=False)
