from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.education_system import Grade
from app.schemas import GradeCreate, GradeUpdate
from app.utils.crud_base import CRUDBase


class CRUDGrade(CRUDBase[Grade, GradeCreate, GradeUpdate]):
    def get_all(self, db: Session, *, skip: int = 0, limit: int = 1000) -> List[Grade]:
        return db.scalars(select(Grade).where(Grade.parent_id == None).offset(skip).limit(limit)).all()


grade = CRUDGrade(model=Grade)
