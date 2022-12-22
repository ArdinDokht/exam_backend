from urllib import request

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.testing import db

from app import schemas, crud, enums
from app.dependencies import get_db
from app.models import Exam
from app.models.exam import ExamQuestion, ExamLesson

router = APIRouter()


@router.post("/", response_model=schemas.Exam)
def create_exam(*, db: Session = Depends(get_db), exam_in: schemas.ExamCreate):
    exam = crud.exam.create(db, obj_in=exam_in)
    return exam


@router.get("/", response_model=list[schemas.Exam])
def get_all_exams(*, db: Session = Depends(get_db)):
    exams = crud.exam.get_all(db)
    return exams


@router.get("/{exam_id}", response_model=schemas.Exam)
def get_exam(*, db: Session = Depends(get_db), exam_id):
    exam = crud.exam.get(db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam


@router.get("/{exam_id}/questions/", response_model=list[schemas.ExamQuestion])
def get_exam_questions(*, db: Session = Depends(get_db), exam_id):
    exam = crud.exam.get(db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return db.scalars(select(ExamQuestion).join(ExamLesson).join(Exam).where(Exam.id == exam_id)).all()


@router.post("/{exam_id}/questions/advance/")
def create_exam_question_advance(*, db: Session = Depends(get_db), exam_id, exam_question_in: schemas.ExamQuestionAdvanceCreate):
    exam = crud.exam.get(db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    exam_lesson = db.execute(
        select(ExamLesson)
        .where(ExamLesson.exam_id == exam_id).where(ExamLesson.lesson_id == exam_question_in.lesson_id)
    ).scalar()

    if exam_lesson is None:
        db_obj = ExamLesson(exam_id=exam.id, lesson_id=exam_question_in.lesson_id, coefficient=0, type=enums.ExamLessonType.GENERAL, duration=0)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        exam_lesson = db_obj

    exam_question = ExamQuestion(exam_lesson=exam_lesson, question_text=exam_question_in.question_text,
                                 answer_text=exam_question_in.answer_text,
                                 type=exam_question_in.type, topic_id=exam_question_in.topic_id, question_number=exam_question_in.question_number,
                                 score=exam_question_in.score)

    db.add(exam_question)
    db.commit()
    db.refresh(exam_question)
    return exam_question
