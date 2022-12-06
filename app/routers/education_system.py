from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.dependencies import get_db

router = APIRouter()


@router.get("/grades/", response_model=list[schemas.Grade])
def read_grades(db: Session = Depends(get_db)):
    res = crud.education_system.get_grades(db)
    return res
