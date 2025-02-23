import typing

from pydantic import Field, ValidationError, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from ragbot.types.logging import LogLevel


class TinydbContextStorageConfig(BaseSettings):
    db_path: str
    table_name: str


class DiscordConfig(BaseSettings):
    token: str


class IRCConfig(BaseSettings):
    host: str
    port: int
    nickname: str
    channels: typing.List[str] = []


class OpenAIConfig(BaseSettings):
    api_key: str
    model: str = "gpt-4o-mini"
    embedding_model: (
        typing.Literal[
            "text-embedding-ada-002",
            "text-embedding-3-small",
            "text-embedding-3-large",
        ]
        | None
    ) = "text-embedding-3-small"
    temperature: float = 0.5
    max_tokens: int = 2500


class MistralAIConfig(BaseSettings):
    model: str = "mistral-small-latest"
    api_key: str
    temperature: float = 0.5
    max_tokens: int = 2500


class JinaConfig(BaseSettings):
    api_key: str
    api_endpoint: str = "https://api.jina.ai/v1/embeddings"


class MilvusConfig(BaseSettings):
    uri: str | None = None
    collection_name: str | None = None
    vector_dim: int | None = None


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

    # Domain:
    domain_module_path: str

    # RAG:
    rag_retrieval_limit: int = Field(default=5)

    # Context storage:
    tinydb: TinydbContextStorageConfig

    # Chat client backend:
    chat_backend: typing.Literal["irc", "discord"]

    # AI chat backend:
    ai_chat_backend: typing.Literal["openai", "mistralai"]

    # Embeddings backend:
    embeddings_backend: typing.Literal["openai", "jina"]

    # Discord:
    discord: DiscordConfig | None = None

    # IRC:
    irc: IRCConfig | None = None

    # OpenAI:
    openai: OpenAIConfig | None = None

    # MistralAI:
    mistralai: MistralAIConfig | None = None

    # Jina:
    jina: JinaConfig | None = None

    # Milvus:
    milvus: MilvusConfig

    @model_validator(mode="after")
    def chat_backend_must_be_configured(self) -> "RagbotConfig":
        """
        Validates that the chat backend is configured correctly.
        """
        if self.chat_backend == "discord" and not self.discord:
            raise ValidationError('"discord" must be present if "chat_backend" is "discord"')
        if self.chat_backend == "irc" and not self.irc:
            raise ValidationError('"irc" must be present if "chat_backend" is "irc"')
        return self

    @model_validator(mode="after")
    def ai_chat_backend_must_be_configured(self) -> "RagbotConfig":
        """
        Validates that the AI chat backend is configured correctly.
        """
        if self.ai_chat_backend == "openai" and not self.openai:
            raise ValidationError('"openai" must be present if "ai_chat_backend" is "openai"')
        if self.ai_chat_backend == "mistralai" and not self.mistralai:
            raise ValidationError('"mistralai" must be present if "ai_chat_backend" is "mistralai"')
        return self

    @model_validator(mode="after")
    def embeddings_backend_must_be_configured(self) -> "RagbotConfig":
        """
        Validates that the embeddings backend is configured
        """
        if self.embeddings_backend == "jina" and not self.jina:
            raise ValidationError('"jina" must be present if "embeddings_backend" is "jina"')
        if self.embeddings_backend == "openai" and not self.openai:
            raise ValidationError('"openai" must be present if "embeddings_backend" is "openai"')
        return self

    @model_validator(mode="before")
    def ignore_unused_backends(cls, values: dict[str, typing.Any]) -> dict[str, typing.Any]:
        """
        Set unused backends to 'None' to avoid unnecessary config errors.
        """

        chat_backend = values.get("chat_backend")
        ai_chat_backend = values.get("ai_chat_backend")
        embeddings_backend = values.get("embeddings_backend")

        if chat_backend == "discord":
            values["irc"] = None
        elif chat_backend == "irc":
            values["discord"] = None

        if "openai" not in [ai_chat_backend, embeddings_backend]:
            values["openai"] = None

        if ai_chat_backend == "openai":
            values["mistralai"] = None

        elif embeddings_backend == "openai":
            values["jina"] = None

        return values
