from pydantic import BaseModel


class LessonParentBase(BaseModel):
    title: str


class LessonParentCreate(LessonParentBase):
    pass


class LessonParentUpdate(LessonParentBase):
    pass


class LessonParent(LessonParentBase):
    id: int

    class Config:
        orm_mode = True
