import datetime
from typing import Optional

from pydantic import BaseModel

from app import enums, schemas
from app.schemas.education_system import GradeWithParent
from app.schemas.lesson import LessonSimple, ExamUserQuestionLesson
from app.schemas.user import User


class ExamBase(BaseModel):
    title: str
    type: enums.ExamType
    start_datetime: datetime.datetime
    duration: int
    question_paper_type: Optional[enums.QuestionPaperType]


class ExamCreate(ExamBase):
    grade_id: int


class ExamUpdate(ExamBase):
    pass


class Exam(ExamBase):
    id: int
    grade: GradeWithParent

    class Config:
        orm_mode = True


class ExamLesson(BaseModel):
    id: int
    exam: Exam
    lesson: LessonSimple

    class Config:
        orm_mode = True


class ExamQuestion(BaseModel):
    id: int
    exam_lesson: ExamLesson
    question_text: str
    answer_text: str
    type: enums.TypeQuestion
    topic: schemas.Topic
    question_number: int
    score: int

    class Config:
        orm_mode = True


class ExamQuestionAdvanceCreate(BaseModel):
    lesson_id: int
    question_text: str
    answer_text: Optional[str]
    type: enums.TypeQuestion
    topic_id: int
    question_number: int
    score: int


class ExamQuestionAdvanceUpdate(BaseModel):
    lesson_id: int
    question_text: str
    answer_text: Optional[str]
    type: enums.TypeQuestion
    topic_id: int
    question_number: int
    score: int


class ExamUserQuestion(BaseModel):
    exam_question_id: int
    question_number: int
    score: Optional[float]
    lesson: ExamUserQuestionLesson

    class Config:
        orm_mode = True


class ExamUserQuestionBulkUpdate(BaseModel):
    exam_question_id: int
    score: Optional[float]


class ExamUser(BaseModel):
    exam: Exam
    user: User

    class Config:
        orm_mode = True
