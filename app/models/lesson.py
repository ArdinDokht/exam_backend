from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from app.models.question import Question
from app.models.education_system import lesson_grade, Grade


class Lesson(Base):
    __tablename__ = "lesson_lesson"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    grades: Mapped[list["Grade"]] = relationship(secondary=lesson_grade, back_populates="lessons")

    topics: Mapped[list["Topic"]] = relationship(back_populates="lesson")

    questions: Mapped[list["Question"]] = relationship(back_populates="lesson")


class Topic(Base):
    __tablename__ = 'lesson_topic'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    lesson_id: Mapped[int] = mapped_column(ForeignKey("lesson_lesson.id"))
    lesson: Mapped["Lesson"] = relationship(back_populates="topics")

    questions: Mapped[list["Question"]] = relationship(back_populates="topic")
