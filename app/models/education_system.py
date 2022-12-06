from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from app.enums.education_system import BaseGrade


class Grade(Base):
    __tablename__ = 'education_system_grade'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    base_grade: Mapped[BaseGrade]

    # Self
    parent_id = mapped_column(ForeignKey("education_system_grade.id"))
    children = relationship("Grade")
