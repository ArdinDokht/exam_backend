from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.education_system import Grade


def get_grades(db: Session):
    stmt = select(Grade).where(Grade.parent_id == None)
    return db.scalars(stmt).all()
