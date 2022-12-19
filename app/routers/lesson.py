from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.dependencies import get_db

router = APIRouter()


@router.get('/', response_model=list[schemas.Lesson])
def read_lessons(db: Session = Depends(get_db)):
    response = crud.lesson.get_all(db)
    return response
