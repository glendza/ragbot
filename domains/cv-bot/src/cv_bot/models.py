from pydantic import BaseModel, RootModel


class WorkExperienceEntry(BaseModel):
    company: str
    title: str
    start_date: str
    end_date: str
    location: str | None
    description: str
    tech_stack: list[str]
    achievements: list[str]


class WorkExperience(RootModel[WorkExperienceEntry]):
    root: list[WorkExperienceEntry]
