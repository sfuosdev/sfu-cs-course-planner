from pydantic import BaseModel, ConfigDict
from app.schemas.courses import CourseSummary
from pydantic.alias_generators import to_camel

class PlanCourseCreate(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel,
                              populate_by_name=True)

    course_id: int
    term_code: int

class PlanCourseUpdate(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel,
                              populate_by_name=True)

    term_code: int

class PlanCourseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)

    id: int
    course: CourseSummary
    term_code: int