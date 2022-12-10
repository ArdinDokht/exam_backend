from app.models import LessonParent, Lesson
from app.schemas import LessonParentCreate, LessonParentUpdate, LessonCreate, LessonUpdate

from app.utils.crud_base import CRUDBase


class CRUDLessonParent(CRUDBase[LessonParent, LessonParentCreate, LessonParentUpdate]):
    pass


class CRUDLesson(CRUDBase[Lesson, LessonCreate, LessonUpdate]):
    pass


lesson_parent = CRUDLessonParent(model=LessonParent)
lesson = CRUDLesson(model=Lesson)
