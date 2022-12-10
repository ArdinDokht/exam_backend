from turtle import back
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base

if TYPE_CHECKING:
    from app.models.education_system import Grade


class LessonParent(Base):
    __tablename__ = "lesson_lesson_parent"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    lessons: Mapped[list["Lesson"]] = relationship(back_populates="lesson_parent")


lesson_topic = Table(
    "lesson_association_lesson_topic",
    Base.metadata,
    Column("lesson_id", ForeignKey("lesson_lesson.id"), primary_key=True),
    Column("topic_id", ForeignKey("lesson_topic.id"), primary_key=True),
)

lesson_target = Table(
    "lesson_association_lesson_target",
    Base.metadata,
    Column("lesson_id", ForeignKey("lesson_lesson.id"), primary_key=True),
    Column("target_id", ForeignKey("lesson_target.id"), primary_key=True),
)


class Lesson(Base):
    __tablename__ = "lesson_lesson"

    id: Mapped[int] = mapped_column(primary_key=True)

    lesson_parent_id: Mapped[int] = mapped_column(ForeignKey("lesson_lesson_parent.id"))
    lesson_parent: Mapped["LessonParent"] = relationship(back_populates="lessons")

    grade_id: Mapped[int] = mapped_column(ForeignKey("education_system_grade.id"))
    grade: Mapped["Grade"] = relationship(back_populates="lessons")

    topics: Mapped[list["Topic"]] = relationship(secondary=lesson_topic, back_populates="lessons")
    targets: Mapped[list["Target"]] = relationship(secondary=lesson_target, back_populates="lessons")


class Topic(Base):
    __tablename__ = 'lesson_topic'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    lessons: Mapped[list["Lesson"]] = relationship(secondary=lesson_topic, back_populates="topics")


class Target(Base):
    __tablename__ = 'lesson_target'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    lessons: Mapped[list["Lesson"]] = relationship(secondary=lesson_target, back_populates="targets")
