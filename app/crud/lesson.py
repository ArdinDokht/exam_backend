from app.models import Lesson
from app.schemas import LessonCreate, LessonUpdate

from app.utils.crud_base import CRUDBase


class CRUDLesson(CRUDBase[Lesson, LessonCreate, LessonUpdate]):
    pass


lesson = CRUDLesson(model=Lesson)
