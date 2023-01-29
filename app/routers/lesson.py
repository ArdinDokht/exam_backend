from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas, crud
from app.dependencies import get_db, get_current_active_staff_user
from app.models import Lesson, Grade, User

router = APIRouter()


@router.get('/', response_model=list[schemas.Lesson])
def read_lessons(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_staff_user), grades: list = Query(default=[])):
    if grades:
        # db.scalars(select(Lesson).where(Lesson.grades.any(id=grade))).all()
        return db.scalars(select(Lesson).where(Lesson.grades.any(Grade.id.in_(grades)))).all()

    response = crud.lesson.get_all(db)
    return response
