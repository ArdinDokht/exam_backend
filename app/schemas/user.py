from pydantic import BaseModel

from app import schemas


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str


class Agency(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserHeaderPrint(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    grade: schemas.Grade
    classroom: schemas.ClassRoom
    agency: Agency

    class Config:
        orm_mode = True
