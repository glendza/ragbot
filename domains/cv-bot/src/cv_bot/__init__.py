from pathlib import Path

from .conversational_schema import CONVERSATIONAL_SCHEMA
from .models import WorkExperience


def get_conversational_schema() -> str:
    return CONVERSATIONAL_SCHEMA


def get_knowledge_base() -> list[str]:
    # Get the knowledge base from the experience.json file:
    experience_json_location = Path(__file__).parent / "data" / "experience.json"
    with open(experience_json_location) as f:
        experience_json = f.read()

    work_experience = WorkExperience.model_validate_json(experience_json)
    return [x.model_dump_json() for x in work_experience.root]
