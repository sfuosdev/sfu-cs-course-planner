from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.models.base import Base

class ProgramRequirement(Base):
    __tablename__ = "program_requirements"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    program_code: Mapped[str] = mapped_column(
        String(20)
    )

    name: Mapped[str] = mapped_column(
        String(255)
    )

    min_courses: Mapped[Optional[int]] = mapped_column(
        Integer
    )

    min_credits: Mapped[Optional[int]] = mapped_column(
        Integer
    )

    courses: Mapped[list["ProgramRequirementCourse"]] = relationship(
        back_populates="program_requirement",
        cascade="all, delete-orphan"
    )
