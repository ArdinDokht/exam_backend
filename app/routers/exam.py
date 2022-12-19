from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Exam)
def create_exam(*, db: Session = Depends(get_db), exam_in: schemas.ExamCreate):
    exam = crud.exam.create(db, obj_in=exam_in)
    return exam


@router.get("/", response_model=list[schemas.Exam])
def get_all_exams(*, db: Session = Depends(get_db)):
    exams = crud.exam.get_all(db)
    return exams

# @router.get("/", response_model=List[schemas.Item])
# def read_items(
#     db: Session = Depends(deps.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Retrieve items.
#     """
#     if crud.user.is_superuser(current_user):
#         items = crud.item.get_multi(db, skip=skip, limit=limit)
#     else:
#         items = crud.item.get_multi_by_owner(
#             db=db, owner_id=current_user.id, skip=skip, limit=limit
#         )
#     return items
