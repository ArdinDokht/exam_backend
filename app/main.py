import json

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from app.config.base import settings
from app.dependencies import get_db
from app.models import User, School, Agency, ClassRoom
from app.routers import education_system, lesson, question, exam

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(db: Session = Depends(get_db)):
    # f = open('./data/sevom_diff_2.json')
    # data = json.load(f)
    #
    # for i in data:
    #     school = db.scalars(select(School).filter_by(token=str(i['School_Id'])).limit(1)).first()
    #     if not school:
    #         db_school = School(title=i['MEMBER_SCHOOL_NAME_VC'], token=str(i['School_Id']))
    #         db.add(db_school)
    #         db.commit()
    #         db.refresh(db_school)
    #         school = db_school
    #
    #     agency = db.scalars(select(Agency).filter_by(token=str(i['Agency_Id'])).limit(1)).first()
    #     if not agency:
    #         db_agency = Agency(name=i['AGENCY_NAME_VC'], token=str(i['Agency_Id']))
    #         db.add(db_agency)
    #         db.commit()
    #         db.refresh(db_agency)
    #         agency = db_agency
    #
    #     class_room = db.scalars(select(ClassRoom).filter_by(token=str(i['classId'])).limit(1)).first()
    #     if not class_room:
    #         db_class_room = ClassRoom(title=i['ClassName'], token=str(i['classId']), school_id=school.id)
    #         db.add(db_class_room)
    #         db.commit()
    #         db.refresh(db_class_room)
    #         class_room = db_class_room
    #
    #     db_user = User(
    #         first_name=i['MEMBER_FIRST_NAME_VC'],
    #         last_name=i['MEMBER_LAST_NAME_VC'],
    #         username=i['Username'],
    #         password=i['Password'],
    #         token=str(i['Id']),
    #         grade_id=i['EDUCATIONAL_SYSTEM_ID'],
    #         agency_id=agency.id,
    #         classroom_id=class_room.id
    #     )
    #     db.add(db_user)
    #     db.commit()
    #     db.refresh(db_user)

    return {"message": "Hello World"}


app.include_router(education_system.router, prefix="/grades", tags=['Education System'])
app.include_router(lesson.router, prefix="/lessons", tags=['Lesson'])
app.include_router(question.router, prefix="/questions", tags=['Question'])
app.include_router(exam.router, prefix="/exam")

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=9000)
