import datetime
from typing import Optional

from pyasn1.compat import integer
from pydantic import BaseModel

from app import enums, schemas
from app.schemas.education_system import GradeWithParent
from app.schemas.lesson import LessonSimple, ExamUserQuestionLesson
from app.schemas.user import User, UserHeaderPrint


class ExamBase(BaseModel):
    title: str
    type: enums.ExamType
    start_datetime: datetime.datetime
    duration: int
    question_paper_type: Optional[enums.QuestionPaperType]


class ExamCreate(ExamBase):
    grade_id: int


class ExamUpdate(ExamBase):
    grade_id: int


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


class ExamLessonSimple(BaseModel):
    id: int
    coefficient: int
    type: enums.ExamLessonType
    duration: Optional[int]
    lesson: LessonSimple

    class Config:
        orm_mode = True


class ExamQuestion(BaseModel):
    id: int
    exam_lesson: ExamLesson
    question_text: str
    answer_text: Optional[str]
    type: enums.TypeQuestion
    topic: schemas.Topic
    question_number: int
    score: float

    class Config:
        orm_mode = True


class ExamQuestionPrint(BaseModel):
    id: int
    question_text: str
    question_number: int
    exam_lesson_id: int

    class Config:
        orm_mode = True


class ExamQuestionAdvanceCreate(BaseModel):
    lesson_id: int
    question_text: str
    answer_text: Optional[str]
    type: enums.TypeQuestion
    topic_id: int
    question_number: int
    score: float


class ExamQuestionAdvanceUpdate(BaseModel):
    lesson_id: int
    question_text: str
    answer_text: Optional[str]
    type: enums.TypeQuestion
    topic_id: int
    question_number: int
    score: float


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


class ExamHeaderPrint(BaseModel):
    id: int
    grade: GradeWithParent
    title: str
    duration: int

    class Config:
        orm_mode = True


class ExamUserHeaderPrint(BaseModel):
    id: int
    created_at: datetime.datetime
    exam: ExamHeaderPrint
    user: UserHeaderPrint

    class Config:
        orm_mode = True
