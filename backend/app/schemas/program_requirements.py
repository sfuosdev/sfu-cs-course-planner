from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.program_requirement_course import ProgramRequirementCourseRead

from pydantic.alias_generators import to_camel

class ProgramRequirementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)

    id: int
    program_code: str
    name: str
    min_credits: Optional[int] = None
    min_courses: Optional[int] = None
    courses: list[ProgramRequirementCourseRead]
