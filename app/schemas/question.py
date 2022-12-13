from typing import Optional

from pydantic import BaseModel

from app import enums
from app.schemas.lesson import Topic, LessonSimple


class QuestionBase(BaseModel):
    question_text: str
    answer_text: Optional[str] = None
    type: enums.TypeQuestion


class QuestionCreate(QuestionBase):
    lesson_id: int
    topic_id: int


class QuestionUpdate(QuestionBase):
    pass


class Question(QuestionBase):
    id: int
    lesson: LessonSimple
    topic: Topic

    class Config:
        orm_mode = True
