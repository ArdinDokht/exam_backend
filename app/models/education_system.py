from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from app import enums
from app.config.database import Base

if TYPE_CHECKING:
    from app.models.lesson import Lesson

lesson_grade = Table(
    "association_lesson_grade",
    Base.metadata,
    Column("lesson_id", ForeignKey("lesson_lesson.id"), primary_key=True),
    Column("grade_id", ForeignKey("education_system_grade.id"), primary_key=True),
)


class Grade(Base):
    __tablename__ = 'education_system_grade'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    base_grade: Mapped[enums.BaseGrade]

    # Self
    parent_id = mapped_column(ForeignKey("education_system_grade.id"))
    children = relationship("Grade", backref=backref("parent", remote_side=[id]))

    # Lesson
    lessons: Mapped[list["Lesson"]] = relationship(secondary=lesson_grade, back_populates="grades")
