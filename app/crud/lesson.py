from app.models import LessonParent
from app.schemas import LessonParentCreate, LessonParentUpdate

from app.utils.crud_base import CRUDBase


class CRUDLessonParent(CRUDBase[LessonParent, LessonParentCreate, LessonParentUpdate]):
    pass


lesson_parent = CRUDLessonParent(model=LessonParent)
