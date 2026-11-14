# app/schemas/__init__.py
from app.schemas.courses import CourseResponse, CourseSummary, ErrorResponse, PrerequisiteRead
from app.schemas.plan import PlanCreate, PlanDetailResponse, PlanResponse, PlanUpdate
from app.schemas.plan_courses import PlanCourseCreate, PlanCourseRead, PlanCourseUpdate
from app.schemas.program_requirement_course import ProgramRequirementCourseRead
from app.schemas.program_requirements import ProgramRequirementResponse
from app.schemas.terms import TermRead
