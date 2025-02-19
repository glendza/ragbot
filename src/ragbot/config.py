import typing

from pydantic import Field, ValidationError, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from ragbot.types.logging import LogLevel


class TinydbContextStorageConfig(BaseSettings):
    db_path: str
    table_name: str


class DiscordConfig(BaseSettings):
    token: str | None = None


class OpenAIConfig(BaseSettings):
    api_key: str | None = None
    model: str = "gpt-4o-mini"
    embedding_model: (
        typing.Literal[
            "text-embedding-ada-002",
            "text-embedding-3-small",
            "text-embedding-3-large",
        ]
        | None
    ) = None
    temperature: float = 0.5
    max_tokens: int = 2500


class MistralAIConfig(BaseSettings):
    model: str = "mistral-small-latest"
    api_key: str | None = None
    temperature: float = 0.5
    max_tokens: int = 2500


class JinaConfig(BaseSettings):
    api_key: str | None = None
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

    # Discord:
    discord: DiscordConfig

    # AI chat backend:
    ai_chat_backend: typing.Literal["openai", "mistralai"]

    # Embeddings backend:
    embeddings_backend: typing.Literal["openai", "jina"]

    # OpenAI:
    openai: OpenAIConfig

    # MistralAI:
    mistralai: MistralAIConfig

    # Jina:
    jina: JinaConfig

    # Milvus:
    milvus: MilvusConfig

    @model_validator(mode="after")
    def validate_ai_chat_backend_configured(self) -> "RagbotConfig":
        if self.ai_chat_backend == "openai":
            if not self.openai.api_key:
                raise ValidationError('"openai.api_key" must be present if "ai_chat_backend" is "openai"')
            if not self.openai.model:
                raise ValidationError('"openai.model" must be present if "ai_chat_backend" is "openai"')
        return self

    @model_validator(mode="after")
    def validate_ai_chat_backend_configured_mistralai(self) -> "RagbotConfig":
        if self.ai_chat_backend == "mistralai":
            if not self.mistralai.api_key:
                raise ValidationError('"mistralai.api_key" must be present if "ai_chat_backend" is "mistralai"')
            if not self.mistralai.model:
                raise ValidationError('m"istralai.model" must be present if "ai_chat_backend" is "mistralai"')
        return self

    @model_validator(mode="after")
    def validate_openai_embeddings_configured(self) -> "RagbotConfig":
        if self.embeddings_backend == "openai":
            if not self.openai.api_key:
                raise ValidationError('"openai.api_key" must be present if "embeddings_backend" is "openai"')
            if not self.openai.embedding_model:
                raise ValidationError('"openai.embedding_model" must be present if "embeddings_backend" is "openai"')
        return self

    @model_validator(mode="after")
    def validate_jina_configured(self) -> "RagbotConfig":
        if self.embeddings_backend == "jina":
            if not self.jina.api_key:
                raise ValidationError('"jina.api_key" must be present')
        return self
