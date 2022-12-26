from urllib import request

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, aliased
from sqlalchemy.testing import db

from app import schemas, crud, enums
from app.dependencies import get_db
from app.models import Exam
from app.models.exam import ExamQuestion, ExamLesson, ExamUser, ExamUserQuestion

router = APIRouter()


# ---------------- Exam Routers -------------------- #

@router.post("/", response_model=schemas.Exam, tags=["Exam"])
def create_exam(*, db: Session = Depends(get_db), exam_in: schemas.ExamCreate):
    exam = crud.exam.create(db, obj_in=exam_in)
    return exam


@router.get("/", response_model=list[schemas.Exam], tags=["Exam"])
def get_all_exams(*, db: Session = Depends(get_db)):
    exams = crud.exam.get_all(db)
    return exams


@router.get("/{exam_id}", response_model=schemas.Exam, tags=["Exam"])
def get_exam(*, db: Session = Depends(get_db), exam_id):
    exam = crud.exam.get(db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam


@router.put("/{exam_id}", response_model=schemas.Exam, tags=["Exam"])
def update_exam(*, db: Session = Depends(get_db), exam_id, exam_in: schemas.ExamUpdate):
    exam = crud.exam.get(db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    exam = crud.exam.update(db, db_obj=exam, obj_in=exam_in)
    return exam


# ---------------- ExamQuestion Routers -------------------- #


@router.get("/{exam_id}/questions/", response_model=list[schemas.ExamQuestion], tags=["ExamQuestion"])
def get_exam_questions(*, db: Session = Depends(get_db), exam_id):
    exam = crud.exam.get(db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return db.scalars(select(ExamQuestion).join(ExamLesson).join(Exam).where(Exam.id == exam_id)).all()


@router.put("/{exam_id}/questions/{exam_question_id}/advance/", tags=["ExamQuestion"], response_model=schemas.ExamQuestion)
def update_exam_question_advance(*, db: Session = Depends(get_db), exam_question_id, exam_id, exam_question_in: schemas.ExamQuestionAdvanceUpdate):
    # Todo add check exam_id in this question
    exam = crud.exam.get(db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    exam_question = db.get(ExamQuestion, exam_question_id)
    if not exam_question:
        raise HTTPException(status_code=404, detail="ExamQuestion not found")

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

    exam_question.exam_lesson = exam_lesson
    exam_question.question_text = exam_question_in.question_text
    exam_question.answer_text = exam_question_in.answer_text
    exam_question.type = exam_question_in.type
    exam_question.topic_id = exam_question_in.topic_id
    exam_question.question_number = exam_question_in.question_number
    exam_question.score = exam_question_in.score

    db.add(exam_question)
    db.commit()
    db.refresh(exam_question)
    return exam_question


@router.post("/{exam_id}/questions/advance/", tags=["ExamQuestion"])
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

    exam_question = ExamQuestion(exam_lesson=exam_lesson,
                                 question_text=exam_question_in.question_text,
                                 answer_text=exam_question_in.answer_text,
                                 type=exam_question_in.type,
                                 topic_id=exam_question_in.topic_id,
                                 question_number=exam_question_in.question_number,
                                 score=exam_question_in.score)

    db.add(exam_question)
    db.commit()
    db.refresh(exam_question)
    return exam_question


# ---------------- ExamUserQuestion Routers -------------------- #

@router.get("/{exam_id}/users/{user_id}/questions/", response_model=list[schemas.ExamUserQuestion], tags=["ExamUserQuestion"])
def get_all_question_users(*, db: Session = Depends(get_db), exam_id, user_id):
    try:
        exam_user = db.execute(select(ExamUser).filter_by(user_id=user_id, exam_id=exam_id)).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="ExamUser not found")

    cte_obj = select(ExamQuestion).join(ExamLesson, isouter=True).where(ExamLesson.exam_id == exam_id).cte()
    exam_questions_cte = aliased(ExamQuestion, cte_obj)

    cte_obj_exam_user_question = select(ExamUserQuestion).filter_by(exam_user=exam_user).cte()
    exam_user_question_cte = aliased(ExamUserQuestion, cte_obj_exam_user_question)

    stmt = select(exam_user_question_cte, exam_questions_cte).join_from(exam_user_question_cte, exam_questions_cte, isouter=True, full=True)
    response = db.execute(stmt).all()
    for user_question, exam_question in response:
        yield {
            'exam_question_id': exam_question.id,
            'question_number': exam_question.question_number,
            'score': user_question.score if user_question else None
        }
