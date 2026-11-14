"""Schemas for course data returned by the SFU course data integration."""

from pydantic import BaseModel, ConfigDict, Field


class PrerequisiteNode(BaseModel):
    """A node in the upstream prerequisite expression tree."""

    model_config = ConfigDict(extra="allow")

    type: str | None = None
    id: str | None = None
    children: list["PrerequisiteNode"] = Field(default_factory=list)


class CourseOffering(BaseModel):
    """A term in which the course is offered."""

    model_config = ConfigDict(extra="allow")

    term: str | None = None
    instructors: list[str] = Field(default_factory=list)


class Course(BaseModel):
    """Normalized course outline data used by the planner."""

    model_config = ConfigDict(extra="allow")

    dept: str
    number: str
    title: str
    units: str | None = None
    description: str = ""
    prerequisites: str = ""
    prerequisite_tree: PrerequisiteNode | None = None
    corequisites: str = ""
    offerings: list[CourseOffering] = Field(default_factory=list)
