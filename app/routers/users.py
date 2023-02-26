import time

from fastapi import APIRouter, Depends, Cookie
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas
from app.dependencies import get_db, get_current_active_user
from app.models import User, Agency

router = APIRouter()


@router.get('/me')
def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post('/', response_model=schemas.User)
def create_user(*, db: Session = Depends(get_db), user_in: schemas.UserCreate):
    obj_data = jsonable_encoder(user_in)
    db_obj = User(**obj_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get('/agency', response_model=list[schemas.Agency])
def get_all_agency(*, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return db.scalars(select(Agency)).all()
