from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from ragbot.types.logging import LogLevel


class DiscordConfig(BaseSettings):
    token: str | None = None


class RagbotConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
        case_sensitive=False,
        env_prefix="RAGBOT__",
        env_nested_delimiter="__",
        frozen=True,
    )

    # Logging:
    log_level: LogLevel = Field(default="INFO")

    # Discord:
    discord: DiscordConfig
