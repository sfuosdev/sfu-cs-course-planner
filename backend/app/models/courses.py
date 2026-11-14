from typing import Optional
from datetime import datetime

from sqlalchemy import String, Integer, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.models.base import Base

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(255)
    )

    course_code: Mapped[str] = mapped_column(
        String(20),
        unique=True
    )

    credits: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    @validates("credits")
    def _missing_credits_become_zero(self, key, value):
        return 0 if value is None else value

    description: Mapped[Optional[str]] = mapped_column(
        Text
    )

    last_synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default=func.now()
    )

    degree_level: Mapped[Optional[str]] = mapped_column(
        String(20)
    )

    corequisites_text:Mapped[Optional[str]] = mapped_column(
        Text
    )

    prerequisites: Mapped[list["Prerequisite"]] = relationship(
        foreign_keys="Prerequisite.course_id", back_populates="course"
    )

    designation: Mapped[Optional[str]] = mapped_column(
        String(255)
    )

    prerequisites_text: Mapped[Optional[str]] = mapped_column(
        Text
    )

    