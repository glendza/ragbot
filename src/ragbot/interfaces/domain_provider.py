from typing import Protocol


class DomainProvider(Protocol):
    def get_conversational_schema(self) -> str: ...

    def get_knowledge_base(self) -> str | list[str]: ...
