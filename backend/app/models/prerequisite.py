from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.models.base import Base

class Prerequisite(Base):
    __tablename__ = "prerequisites"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE")
    )

    course: Mapped["Course"] = relationship(
        foreign_keys=[course_id], 
        back_populates="prerequisites"
    )

    required_course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE")
    )

    required_course: Mapped["Course"] = relationship(
        foreign_keys=[required_course_id]
    )

    group_number: Mapped[int] = mapped_column(
        Integer
    )