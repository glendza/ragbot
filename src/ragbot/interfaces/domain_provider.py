from typing import Protocol


class DomainProvider(Protocol):
    def get_knowledge_base(self) -> str | list[str]: ...
