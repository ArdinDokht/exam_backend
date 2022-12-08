from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base

if TYPE_CHECKING:
    from app.models.education_system import Grade


class LessonParent(Base):
    __tablename__ = "lesson_lesson_parent"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    lessons: Mapped[list["Lesson"]] = relationship(back_populates="lesson_parent")


class Lesson(Base):
    __tablename__ = "lesson_lesson"

    id: Mapped[int] = mapped_column(primary_key=True)

    lesson_parent_id: Mapped[int] = mapped_column(ForeignKey("lesson_lesson_parent.id"))
    lesson_parent: Mapped["LessonParent"] = relationship(back_populates="lessons")

    grade_id: Mapped[int] = mapped_column(ForeignKey("education_system_grade.id"))
    grade: Mapped["Grade"] = relationship(back_populates="lessons")
