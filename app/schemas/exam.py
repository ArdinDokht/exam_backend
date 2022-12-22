import datetime

from pydantic import BaseModel

from app import enums, schemas
from app.schemas.education_system import GradeWithParent


class ExamBase(BaseModel):
    title: str
    type: enums.ExamType
    start_datetime: datetime.datetime
    duration: int
    question_paper_type: enums.QuestionPaperType


class ExamCreate(ExamBase):
    grade_id: int


class ExamUpdate(ExamBase):
    pass


class Exam(ExamBase):
    id: int
    grade: GradeWithParent

    class Config:
        orm_mode = True


class ExamQuestion(BaseModel):
    id: int
    exam_lesson_id: int
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
    answer_text: str
    type: enums.TypeQuestion
    topic_id: int
    question_number: int
    score: int
 