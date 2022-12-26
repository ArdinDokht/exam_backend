import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import enums
from app.config.database import Base

if TYPE_CHECKING:
    from app.models import Lesson, Grade, Topic, Question, User


class Exam(Base):
    __tablename__ = 'exam_exam'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    type: Mapped[enums.ExamType]
    question_paper_type: Mapped[enums.QuestionPaperType] = mapped_column(default=enums.QuestionPaperType.FULL)
    start_datetime: Mapped[datetime.datetime]
    duration: Mapped[int]

    # Grade
    grade_id: Mapped[int] = mapped_column(ForeignKey("education_system_grade.id"))
    grade: Mapped["Grade"] = relationship(back_populates="exams")

    # Lesson
    exam_lessons: Mapped[list["ExamLesson"]] = relationship(back_populates="exam")

    # ExamUser
    user_associations: Mapped[list["ExamUser"]] = relationship(back_populates="exam")
    users: Mapped[list["User"]] = relationship(secondary="exam_user", back_populates="exams")


class ExamLesson(Base):
    __tablename__ = 'exam_lesson_exam'

    id: Mapped[int] = mapped_column(primary_key=True)

    exam_id: Mapped[int] = mapped_column(ForeignKey("exam_exam.id"))
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lesson_lesson.id"))

    coefficient: Mapped[int]
    type: Mapped[enums.ExamLessonType]
    duration: Mapped[int] = mapped_column(nullable=True)

    exam: Mapped["Exam"] = relationship(back_populates="exam_lessons")
    lesson: Mapped["Lesson"] = relationship(back_populates="exam_lessons")

    exam_questions: Mapped[list["ExamQuestion"]] = relationship(back_populates="exam_lesson")


class ExamQuestion(Base):
    __tablename__ = 'exam_question'

    id: Mapped[int] = mapped_column(primary_key=True)

    exam_lesson_id: Mapped[int] = mapped_column(ForeignKey("exam_lesson_exam.id"))
    exam_lesson: Mapped["ExamLesson"] = relationship(back_populates="exam_questions")

    question_text: Mapped[str]
    answer_text: Mapped[str] = mapped_column(nullable=True)
    type: Mapped[enums.TypeQuestion]

    topic_id: Mapped[int] = mapped_column(ForeignKey("lesson_topic.id"))
    topic: Mapped["Topic"] = relationship(back_populates="exam_questions")

    question_id: Mapped[int] = mapped_column(ForeignKey("question_question.id"), nullable=True)
    question: Mapped["Question"] = relationship(back_populates="exam_questions")

    question_number: Mapped[int] = mapped_column(default=0)

    score: Mapped[float] = mapped_column(default=0)
    negative_score: Mapped[float] = mapped_column(default=0)

    exam_users: Mapped[list["ExamUserQuestion"]] = relationship(back_populates="exam_question")


class ExamUser(Base):
    __tablename__ = 'exam_user'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user_user.id"))
    exam_id: Mapped[int] = mapped_column(ForeignKey("exam_exam.id"))

    user: Mapped["User"] = relationship(back_populates="exam_associations")

    exam: Mapped["Exam"] = relationship(back_populates="user_associations")

    questions: Mapped[list["ExamUserQuestion"]] = relationship(back_populates="exam_user")


class ExamUserQuestion(Base):
    __tablename__ = 'exam_user_question'
    id: Mapped[int] = mapped_column(primary_key=True)

    exam_user_id: Mapped[int] = mapped_column(ForeignKey("exam_user.id"))
    exam_user: Mapped["ExamUser"] = relationship(back_populates="questions")

    exam_question_id: Mapped[int] = mapped_column(ForeignKey("exam_question.id"))
    exam_question: Mapped["ExamQuestion"] = relationship(back_populates="exam_users")

    answer_image: Mapped[str] = mapped_column(nullable=True)

    score: Mapped[float] = mapped_column(nullable=True)
