from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.dependencies import get_db

router = APIRouter()


@router.get('/', response_model=list[schemas.Lesson])
def read_lessons(db: Session = Depends(get_db)):
    response = crud.lesson.get_all(db)
    return response

# @router.post('/lesson/', response_model=schemas.Lesson)
# def create_lesson(lesson_in: schemas.LessonCreate, db: Session = Depends(get_db)):
#     response = crud.lesson.create(db, obj_in=lesson_in)
#     return response
