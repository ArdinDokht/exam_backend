from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from app import enums
from app.config.database import Base

if TYPE_CHECKING:
    from app.models.lesson import Lesson


class Grade(Base):
    __tablename__ = 'education_system_grade'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    base_grade: Mapped[enums.BaseGrade]

    # Self
    parent_id = mapped_column(ForeignKey("education_system_grade.id"))
    children = relationship("Grade", backref=backref("parent", remote_side=[id]))

    # Lesson
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="grade")
