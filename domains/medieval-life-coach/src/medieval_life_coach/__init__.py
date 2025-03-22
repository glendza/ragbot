from . import knowledge_base
from .conversational_schema import CONVERSATIONAL_SCHEMA


def get_conversational_schema() -> str:
    return CONVERSATIONAL_SCHEMA


def get_knowledge_base() -> list[str]:
    return knowledge_base.get_knowledge_base()
