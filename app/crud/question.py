from app.models.question import Question
from app.schemas import QuestionCreate, QuestionUpdate

from app.utils.crud_base import CRUDBase


class CRUDQuestion(CRUDBase[Question, QuestionCreate, QuestionUpdate]):
    pass


question = CRUDQuestion(model=Question)
