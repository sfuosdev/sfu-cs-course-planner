from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class PlanCourse(Base):
    __tablename__ = "plan_courses"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id")
    )

    course: Mapped["Course"] = relationship()

    plan_id: Mapped[int] = mapped_column(
        ForeignKey("plans.id", ondelete="CASCADE")
    )

    plan: Mapped["Plan"] = relationship(
        back_populates="plan_courses"
    )

    term_code: Mapped[int] = mapped_column(
        ForeignKey("terms.code")
    )

    term: Mapped["Term"] = relationship()