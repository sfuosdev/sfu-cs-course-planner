from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.models.base import Base

class ProgramRequirementCourse(Base):
    __tablename__ = "program_requirement_courses"

    requirement_id: Mapped[int] = mapped_column(
        ForeignKey("program_requirements.id"),
        primary_key=True
    )

    program_requirement: Mapped["ProgramRequirement"] = relationship(
        back_populates="courses"
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id"),
        primary_key=True
    )

    course: Mapped["Course"] = relationship()