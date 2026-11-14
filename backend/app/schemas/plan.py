from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.plan_courses import PlanCourseRead

from pydantic.alias_generators import to_camel
#request
class PlanCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)

class PlanUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    version: int = Field(ge=1, description="The version of the plan to update. Must match the current version of the plan in the database.")

#responses
class PlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                                populate_by_name=True)

    id: int
    name: str
    version: int
    updated_at: datetime
    created_at: datetime

class PlanDetailResponse(PlanResponse):
    plan_courses: list[PlanCourseRead] = []




