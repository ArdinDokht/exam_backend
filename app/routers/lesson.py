from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.dependencies import get_db

router_lesson_parent = APIRouter()
router_lesson = APIRouter()


@router_lesson_parent.get('/lesson/parent/', response_model=list[schemas.LessonParent])
def read_lesson_parents(db: Session = Depends(get_db)):
    return crud.lesson_parent.get_all(db)


@router_lesson_parent.post('/lesson/parent/', response_model=schemas.LessonParent)
def create_lesson_parent(lesson_parent_in: schemas.LessonParentCreate, db: Session = Depends(get_db)):
    response = crud.lesson_parent.create(db, obj_in=lesson_parent_in)
    return response


@router_lesson.get('/lesson/', response_model=list[schemas.Lesson])
def read_lessons(db: Session = Depends(get_db)):
    response = crud.lesson.get_all(db)
    for item in response:
        item.title = item.lesson_parent.title + ' ' + item.grade.title + ' ' + item.grade.base_grade.value
        if item.grade.parent:
            item.title += f'({item.grade.parent.title})'
    return response


@router_lesson.post('/lesson/', response_model=schemas.Lesson)
def create_lesson(lesson_in: schemas.LessonCreate, db: Session = Depends(get_db)):
    response = crud.lesson.create(db, obj_in=lesson_in)
    return response
