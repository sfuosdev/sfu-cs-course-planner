from datetime import datetime

from sqlalchemy import String, func, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    version: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    name: Mapped[str] = mapped_column(
        String(255)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default=func.now(),
        nullable=False
    )

    plan_courses: Mapped[list["PlanCourse"]] = relationship(
        back_populates="plan",
        cascade="all, delete-orphan"
    )
