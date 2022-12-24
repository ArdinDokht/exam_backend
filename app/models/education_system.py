from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from app import enums
from app.config.database import Base

if TYPE_CHECKING:
    from app.models.lesson import Lesson
    from app.models.exam import Exam
    from app.models.user import User

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

    # Exam
    exams: Mapped[list["Exam"]] = relationship(back_populates="grade")

    # User
    users: Mapped[list["User"]] = relationship(back_populates="grade")


class School(Base):
    __tablename__ = 'education_system_school'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    class_rooms: Mapped[list["ClassRoom"]] = relationship(back_populates="school")


class ClassRoom(Base):
    __tablename__ = 'education_system_class_room'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    school_id = mapped_column(ForeignKey("education_system_school.id"))
    school: Mapped["School"] = relationship(back_populates="class_rooms")

    users: Mapped[list["User"]] = relationship(back_populates="classroom")
