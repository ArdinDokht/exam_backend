from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base

if TYPE_CHECKING:
    from app.models.education_system import Grade
    from app.models.exam import Exam, ExamLesson, ExamQuestion
    from app.models.question import Question


class Lesson(Base):
    __tablename__ = "lesson_lesson"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    grades: Mapped[list["Grade"]] = relationship(secondary="association_lesson_grade", back_populates="lessons")

    topics: Mapped[list["Topic"]] = relationship(back_populates="lesson")

    questions: Mapped[list["Question"]] = relationship(back_populates="lesson")

    # Exam
    exam_lessons: Mapped[list["ExamLesson"]] = relationship(back_populates="lesson")
    # exams: Mapped[list["Exam"]] = relationship(secondary="exam_lesson_exam", back_populates="lessons")
    # exam_associations: Mapped[list["ExamLesson"]] = relationship(back_populates="lesson")


class Topic(Base):
    __tablename__ = 'lesson_topic'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    lesson_id: Mapped[int] = mapped_column(ForeignKey("lesson_lesson.id"))
    lesson: Mapped["Lesson"] = relationship(back_populates="topics")

    questions: Mapped[list["Question"]] = relationship(back_populates="topic")

    exam_questions: Mapped[list["ExamQuestion"]] = relationship(back_populates="topic")
