from pydantic import BaseModel, RootModel


class RagSearcResult(BaseModel):
    id: int
    distance: float
    content: str


class RagSearchResults(RootModel[list[RagSearcResult]]):
    root: list[RagSearcResult]
