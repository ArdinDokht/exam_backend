from app.models import Exam
from app.schemas import ExamUpdate, ExamCreate
from app.utils.crud_base import CRUDBase


class CRUDExam(CRUDBase[Exam, ExamCreate, ExamUpdate]):
    pass


exam = CRUDExam(model=Exam)
