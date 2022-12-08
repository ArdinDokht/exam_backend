from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.dependencies import get_db

router = APIRouter()


@router.get('/lesson/parent/', response_model=list[schemas.LessonParent])
def read_lesson_parents(db: Session = Depends(get_db)):
    return crud.lesson_parent.get_all(db)


@router.post('/lesson/parent/', response_model=schemas.LessonParent)
def create_lesson_parent(lesson_parent_in: schemas.LessonParentCreate, db: Session = Depends(get_db)):
    response = crud.lesson_parent.create(db, obj_in=lesson_parent_in)
    return response
