from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from app.models.exam import ExamUser

if TYPE_CHECKING:
    from app.models import Grade, Exam
    from app.models.education_system import ClassRoom


class User(Base):
    __tablename__ = 'user_user'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    token: Mapped[str]

    # Grade
    grade_id: Mapped[int] = mapped_column(ForeignKey("education_system_grade.id"))
    grade: Mapped["Grade"] = relationship(back_populates="users")

    # Agency
    agency_id: Mapped[int] = mapped_column(ForeignKey("user_agency.id"))
    agency: Mapped["Agency"] = relationship(back_populates="users")

    # ClassRoom
    classroom_id: Mapped[int] = mapped_column(ForeignKey("education_system_class_room.id"))
    classroom: Mapped["ClassRoom"] = relationship(back_populates="users")

    exam_associations: Mapped[list["ExamUser"]] = relationship(back_populates="user")
    exams: Mapped[list["Exam"]] = relationship(secondary="exam_user", back_populates="users")


class Agency(Base):
    __tablename__ = 'user_agency'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    token: Mapped[str]

    users: Mapped[list["User"]] = relationship(back_populates="agency")
