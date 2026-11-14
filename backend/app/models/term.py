from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from app.models.base import Base

class Term(Base):
    __tablename__ = "terms"

    code: Mapped[int] = mapped_column(
        primary_key=True,
    )

    year: Mapped[int] = mapped_column(
        Integer
    )

    season: Mapped[str] = mapped_column(
        String(20)
    )

