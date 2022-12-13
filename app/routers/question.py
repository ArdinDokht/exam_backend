from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.dependencies import get_db

router = APIRouter()


@router.get('/', response_model=list[schemas.Question])
def read_questions(db: Session = Depends(get_db)):
    return crud.question.get_all(db)


@router.post('/', response_model=schemas.Question)
def create_question(question_in: schemas.QuestionCreate, db: Session = Depends(get_db)):
    response = crud.question.create(db, obj_in=question_in)
    return response
