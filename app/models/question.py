from typing import TYPE_CHECKING

from sqlalchemy import Enum, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import enums
from app.config.database import Base

if TYPE_CHECKING:
    from app.models import Lesson, Topic


class Question(Base):
    __tablename__ = 'question_question'

    id: Mapped[int] = mapped_column(primary_key=True)
    question_text: Mapped[str]
    answer_text: Mapped[str] = mapped_column(nullable=True)
    type: Mapped[enums.TypeQuestion]

    lesson_id: Mapped[int] = mapped_column(ForeignKey("lesson_lesson.id"))
    lesson: Mapped["Lesson"] = relationship(back_populates="questions")

    topic_id: Mapped[int] = mapped_column(ForeignKey("lesson_topic.id"))
    topic: Mapped["Topic"] = relationship(back_populates="questions")
