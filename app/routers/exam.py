import uuid
from datetime import datetime
from urllib import request

import boto3
import pymssql
# import cairosvg
from fastapi import APIRouter, Depends, HTTPException, Response, UploadFile
from sqlalchemy import select, func, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import Session, aliased
from starlette import status

from app import schemas, crud, enums
from app.core.services import get_images_from_s3_folder, crop_images
from app.dependencies import get_db, get_current_active_staff_user
from app.enums import ExamStatusType, ExamScoreType
from app.models import Exam, User, Grade, Agency, ClassRoom, School, Topic
from app.models.exam import ExamQuestion, ExamLesson, ExamUser, ExamUserQuestion, ExamStatus, ExamUserScore
from app.utils.file_helper import allowed_file

router = APIRouter()


# ---------------- Exam Routers -------------------- #

@router.post("/", response_model=schemas.Exam, tags=["Exam"])
def create_exam(*, db: Session = Depends(get_db), exam_in: schemas.ExamCreate, current_user: User = Depends(get_current_active_staff_user)):
    exam = crud.exam.create(db, obj_in=exam_in)

    db.add(ExamStatus(title='نیاز به تمرین بیشتر', type=ExamStatusType.CLASS_ROOM, start_percent=-100, end_percent=0, exam=exam))
    db.add(ExamStatus(title='قابل قبول', type=ExamStatusType.CLASS_ROOM, start_percent=0, end_percent=50, exam=exam))
    db.add(ExamStatus(title='متوسط خوب', type=ExamStatusType.CLASS_ROOM, start_percent=50, end_percent=65, exam=exam))
    db.add(ExamStatus(title='خوب', type=ExamStatusType.CLASS_ROOM, start_percent=65, end_percent=75, exam=exam))
    db.add(ExamStatus(title='خیلی خوب', type=ExamStatusType.CLASS_ROOM, start_percent=75, end_percent=100, exam=exam))

    db.add(ExamStatus(title='نیاز به تمرین بیشتر', type=ExamStatusType.SCHOOL, start_percent=-100, end_percent=0, exam=exam))
    db.add(ExamStatus(title='قابل قبول', type=ExamStatusType.SCHOOL, start_percent=0, end_percent=50, exam=exam))
    db.add(ExamStatus(title='متوسط خوب', type=ExamStatusType.SCHOOL, start_percent=50, end_percent=65, exam=exam))
    db.add(ExamStatus(title='خوب', type=ExamStatusType.SCHOOL, start_percent=65, end_percent=75, exam=exam))
    db.add(ExamStatus(title='خیلی خوب', type=ExamStatusType.SCHOOL, start_percent=75, end_percent=100, exam=exam))

    db.add(ExamStatus(title='نیاز به تمرین بیشتر', type=ExamStatusType.TOTAL, start_percent=-100, end_percent=25, exam=exam))
    db.add(ExamStatus(title='قابل قبول', type=ExamStatusType.TOTAL, start_percent=25, end_percent=50, exam=exam))
    db.add(ExamStatus(title='خوب', type=ExamStatusType.TOTAL, start_percent=50, end_percent=75, exam=exam))
    db.add(ExamStatus(title='خیلی خوب', type=ExamStatusType.TOTAL, start_percent=75, end_percent=100, exam=exam))

    db.commit()

    return exam


@router.get("/", response_model=list[schemas.Exam], tags=["Exam"])
def get_all_exams(*, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_staff_user)):
    exams = crud.exam.get_all(db)
    return exams


@router.post("/crop", tags=["exam"])
async def crop_exams():
    # Get the images.
    images = get_images_from_s3_folder('scanned_images/')
    await crop_images(images)
    return "Success"


@router.get("/{exam_id}", response_model=schemas.Exam, tags=["Exam"])
def get_exam(*, db: Session = Depends(get_db), exam_id, current_user: User = Depends(get_current_active_staff_user)):
    exam = crud.exam.get(db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam


@router.put("/{exam_id}", response_model=schemas.Exam, tags=["Exam"])
def update_exam(*, db: Session = Depends(get_db), exam_id, exam_in: schemas.ExamUpdate, current_user: User = Depends(get_current_active_staff_user)):
    print(exam_in.start_datetime)
    exam = crud.exam.get(db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    exam = crud.exam.update(db, db_obj=exam, obj_in=exam_in)
    return exam


@router.get("/{exam_id}/print/header", response_model=list[schemas.ExamUserHeaderPrint], tags=["Exam"])
def get_exam_header_print(*, db: Session = Depends(get_db), exam_id, current_user: User = Depends(get_current_active_staff_user)):
    exam_user = db.scalars(select(ExamUser).filter_by(exam_id=exam_id).join(Exam).join(User).join(Grade).join(ClassRoom).join(School)).all()

    return exam_user


@router.get("/sync/", tags=["Exam"])
def before_sync_exam(current_user: User = Depends(get_current_active_staff_user)):
    conn = pymssql.connect('192.168.220.27', 'tosifi_user', 'Tosif@1401', "erp")
    cursor = conn.cursor(as_dict=True)
    cursor.execute(
        f'select * from radb.Tosifi_Exams'
    )

    for row in cursor:
        yield {
            'id': row['examinationId'],
            'title': f'{row["productGroup"]} پایه {row["Title"]} شماره {row["productTitle"]}'
        }


@router.get("/{exam_id}/sync/{remote_id}", tags=["Exam"])
def sync_exam(*, exam_id, remote_id, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_staff_user)):
    conn = pymssql.connect('192.168.220.27', 'tosifi_user', 'Tosif@1401', "erp")
    cursor = conn.cursor(as_dict=True)
    cursor.execute(
        f'select a.Id applicantId,a.MEMBER_FIRST_NAME_VC firstName,a.MEMBER_LAST_NAME_VC lastName,a.EDUCATIONAL_SYSTEM_ID educationalId,a.Agency_Id agencyId ,a.Agency_Id,a.AGENCY_NAME_VC,a.School_Id,a.MEMBER_SCHOOL_NAME_VC,a.AGENCY_BRANCH_ID class_id,a.AGENCY_BRANCH_NAME_VC className,u.Username,u.Password '
        f'from radb.ProductApplicantClass pac '
        f'inner join radb.ApplicantClass ac on ac.id=pac.ApplicantClass_Id '
        f'inner join radb.Applicant a on a.id=ac.Applicant_Id '
        f'inner join radb.[user] u on u.id=a.Id '
        f'where pac.Product_Id={remote_id}'
    )

    for row in cursor:
        new_row = {
            'user_id': row['applicantId'],
            'first_name': row['firstName'],
            'last_name': row['lastName'],
            'username': row['Username'],
            'password': row['Password'],
            'classroom_id': row['class_id'],
            'classroom_title': row['className'],
            'school_id': row['School_Id'],
            'school_title': row['MEMBER_SCHOOL_NAME_VC'],
            'grade_id': row['educationalId'],
            'agency_id': row['agencyId'],
            'agency_title': row['AGENCY_NAME_VC'],
        }
        school = db.scalars(select(School).filter_by(token=str(new_row['school_id'])).limit(1)).first()
        if not school:
            school = School(title=new_row['school_title'], token=str(new_row['school_id']))
            db.add(school)
            db.flush()

        class_room = db.scalars(select(ClassRoom).filter_by(token=str(new_row['classroom_id'])).limit(1)).first()
        if not class_room:
            class_room = ClassRoom(title=new_row['classroom_title'], token=str(new_row['classroom_id']), school_id=school.id)
            db.add(class_room)

        agency = db.scalars(select(Agency).filter_by(token=str(new_row['agency_id'])).limit(1)).first()
        if not agency:
            agency = Agency(name=new_row['agency_title'], token=str(new_row['agency_id']))
            db.add(agency)

        db_user = db.scalars(select(User).filter_by(username=new_row['username']).limit(1)).first()
        if not db_user:
            db_user = User(
                first_name=new_row['first_name'],
                last_name=new_row['last_name'],
                username=new_row['username'],
                password=new_row['password'],
                token=str(new_row['user_id']),
                grade_id=new_row['grade_id'],
                agency_id=agency.id,
                classroom_id=class_room.id
            )
            db.add(db_user)

        try:
            db.execute(select(ExamUser).filter_by(exam_id=exam_id, user=db_user)).scalar_one()
        except NoResultFound:
            db.add(ExamUser(exam_id=exam_id, user=db_user))

    db.commit()
    return {"message": "finished successfully"}


# ---------------- Exam Lesson Routers -------------------- #
@router.get("/{exam_id}/lessons", response_model=list[schemas.ExamLessonSimple], tags=["ExamLesson"])
def get_exam_lessons(*, db: Session = Depends(get_db), exam_id, current_user: User = Depends(get_current_active_staff_user)):
    exam = crud.exam.get(db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    stmt = select(ExamLesson).filter_by(exam=exam).order_by(ExamLesson.id)
    return db.scalars(stmt).all()


@router.put("/{exam_id}/lessons", response_model=list[schemas.ExamLessonSimple], tags=["ExamLesson"])
def update_exam_lessons(*, db: Session = Depends(get_db), exam_id, exam_lessons_in: list[schemas.ExamLessonSimple],
                        current_user: User = Depends(get_current_active_staff_user)):
    exam = crud.exam.get(db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    exam_lessons_db = exam.exam_lessons

    for item in exam_lessons_db:
        item_in = [x for x in exam_lessons_in if x.id == item.id][0]
        item.coefficient = item_in.coefficient
        item.type = item_in.type
        item.duration = item_in.duration

        db.add(item)
        db.commit()
        db.refresh(item)

    return exam_lessons_db

    # ---------------- ExamQuestion Routers -------------------- #


# ---------------- Exam Questions Routers -------------------- #
@router.get("/{exam_id}/questions/", response_model=list[schemas.ExamQuestion], tags=["ExamQuestion"])
def get_exam_questions(*, db: Session = Depends(get_db), exam_id, current_user: User = Depends(get_current_active_staff_user)):
    exam = crud.exam.get(db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return db.scalars(select(ExamQuestion).join(ExamLesson).join(Exam).where(Exam.id == exam_id).order_by(ExamQuestion.question_number)).all()


@router.delete("/{exam_question_id}/", tags=["ExamQuestion"])
def remove_exam_question(*, db: Session = Depends(get_db), exam_question_id, current_user: User = Depends(get_current_active_staff_user)):
    try:
        obj = db.get(ExamQuestion, exam_question_id)
        db.delete(obj)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This question cannot be deleted")

    return obj


@router.post("/image/upload/", tags=["ExamQuestion"])
def upload_image(file: UploadFile, current_user: User = Depends(get_current_active_staff_user)):
    if not allowed_file(file.filename, {'png', 'jpg', 'jpeg'}):
        raise HTTPException(status_code=400, detail="Invalid file type")

    # file_binary = file.read()
    # if len(file_binary) > 10 * 1024 * 1024:  # limit file size to 10MB
    #     raise HTTPException(status_code=400, detail="File size exceeded 10MB limit")

    # mime = magic.from_buffer(file_binary, mime=True)
    # if not mime.startswith("image"):
    #     raise HTTPException(status_code=400, detail="Invalid file format")
    # Save file to AWS S3 storage
    unique_filename = str(uuid.uuid4()) + '_' + file.filename

    s3 = boto3.client("s3",
                      aws_access_key_id="kue698sasgcqqkse",
                      aws_secret_access_key="068be239-c495-43a0-a2af-2df170a79899",
                      endpoint_url="https://storage.iran.liara.space",
                      )
    s3.put_object(Bucket="exam", Key=unique_filename, Body=file.file)

    # svg_code = cairosvg.svg2png(url=file.file)

    # s3.put_object(Bucket="exam", Key=file.filename, Body=svg_code)
    # pre_signed_url = s3.generate_presigned_url(
    #     ClientMethod="get_object",
    #     Params={
    #         "Bucket": "exam",
    #         "Key": file.filename
    #     },
    #     ExpiresIn=3600  # URL valid for one hour
    # )
    # return {"url": pre_signed_url}
    return {"url": f"https://exam.storage.iran.liara.space/{unique_filename}"}


@router.put("/{exam_id}/questions/{exam_question_id}/advance/", tags=["ExamQuestion"], response_model=schemas.ExamQuestion)
def update_exam_question_advance(*, db: Session = Depends(get_db), exam_question_id, exam_id, exam_question_in: schemas.ExamQuestionAdvanceUpdate,
                                 current_user: User = Depends(get_current_active_staff_user)):
    # Todo add check exam_id in this question
    exam = crud.exam.get(db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    exam_question = db.get(ExamQuestion, exam_question_id)
    if not exam_question:
        raise HTTPException(status_code=404, detail="ExamQuestion not found")

    exam_lesson = db.execute(
        select(ExamLesson)
        .where(ExamLesson.exam_id == exam_id).where(ExamLesson.lesson_id == exam_question_in.lesson_id)
    ).scalar()

    if exam_lesson is None:
        db_obj = ExamLesson(exam_id=exam.id, lesson_id=exam_question_in.lesson_id, coefficient=0, type=enums.ExamLessonType.GENERAL)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        exam_lesson = db_obj

    exam_question.exam_lesson = exam_lesson
    exam_question.question_text = exam_question_in.question_text
    exam_question.answer_text = exam_question_in.answer_text
    exam_question.type = exam_question_in.type
    exam_question.topic_id = exam_question_in.topic_id
    exam_question.question_number = exam_question_in.question_number
    exam_question.score = exam_question_in.score

    db.add(exam_question)
    db.commit()
    db.refresh(exam_question)
    return exam_question


@router.post("/{exam_id}/questions/advance/", tags=["ExamQuestion"])
def create_exam_question_advance(*, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_staff_user), exam_id,
                                 exam_question_in: schemas.ExamQuestionAdvanceCreate):
    exam = crud.exam.get(db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    exam_lesson = db.execute(
        select(ExamLesson)
        .where(ExamLesson.exam_id == exam_id).where(ExamLesson.lesson_id == exam_question_in.lesson_id)
    ).scalar()

    if exam_lesson is None:
        db_obj = ExamLesson(exam_id=exam.id, lesson_id=exam_question_in.lesson_id, coefficient=0, type=enums.ExamLessonType.GENERAL)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        exam_lesson = db_obj

    exam_question = ExamQuestion(exam_lesson=exam_lesson,
                                 question_text=exam_question_in.question_text,
                                 answer_text=exam_question_in.answer_text,
                                 type=exam_question_in.type,
                                 topic_id=exam_question_in.topic_id,
                                 question_number=exam_question_in.question_number,
                                 score=exam_question_in.score)

    db.add(exam_question)
    db.commit()
    db.refresh(exam_question)
    return exam_question


@router.get("/{exam_id}/questions/print/", response_model=list[schemas.ExamQuestionPrint], tags=["ExamQuestion"])
def get_exam_questions(*, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_staff_user), exam_id):
    exam = crud.exam.get(db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return db.scalars(select(ExamQuestion).join(ExamLesson).join(Exam).where(Exam.id == exam_id).order_by(ExamQuestion.question_number)).all()


# ---------------- ExamUser Routers -------------------- #

@router.get("/{exam_id}/users/", response_model=list[schemas.User], tags=["ExamUser"])
def get_all_exam_users(*, db: Session = Depends(get_db), exam_id):
    exam = crud.exam.get(db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam.users


# ---------------- ExamUserQuestion Routers -------------------- #

@router.get("/{exam_id}/users/{user_id}/questions/", response_model=list[schemas.ExamUserQuestion], tags=["ExamUserQuestion"])
def get_all_question_users(*, db: Session = Depends(get_db), exam_id, user_id):
    try:
        exam_user = db.execute(select(ExamUser).filter_by(user_id=user_id, exam_id=exam_id)).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="ExamUser not found")

    cte_obj = select(ExamQuestion).join(ExamLesson, isouter=True).where(ExamLesson.exam_id == exam_id).cte()
    exam_questions_cte = aliased(ExamQuestion, cte_obj)

    cte_obj_exam_user_question = select(ExamUserQuestion).filter_by(exam_user=exam_user).cte()
    exam_user_question_cte = aliased(ExamUserQuestion, cte_obj_exam_user_question)

    stmt = select(exam_user_question_cte, exam_questions_cte).join_from(exam_user_question_cte, exam_questions_cte, isouter=True, full=True)
    response = db.execute(stmt).all()
    list_response = []
    for user_question, exam_question in response:
        list_response.append({
            'exam_question_id': exam_question.id,
            'question_number': exam_question.question_number,
            'score': user_question.score if user_question else None,
            'lesson': exam_question.exam_lesson.lesson
        })
    return sorted(list_response, key=lambda x: x['question_number'])


@router.post("/{exam_id}/users/{user_id}/questions/", tags=["ExamUserQuestion"])
def update_questions_user(*, db: Session = Depends(get_db), exam_id, user_id, obj_in: list[schemas.ExamUserQuestionBulkUpdate]):
    try:
        exam_user = db.execute(select(ExamUser).filter_by(user_id=user_id, exam_id=exam_id)).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="ExamUser not found")

    for item in obj_in:
        if not item.score is None:
            try:
                exam_user_question = db.execute(
                    select(ExamUserQuestion).filter_by(exam_user=exam_user, exam_question_id=item.exam_question_id)).scalar_one()
                exam_user_question.score = item.score
                db.add(exam_user_question)
                db.commit()
                # db.refresh(exam_user_question)
                # return exam_user_question
            except NoResultFound:
                db_obj = ExamUserQuestion(exam_user=exam_user, exam_question_id=item.exam_question_id, score=item.score)
                db.add(db_obj)
                db.commit()

    return Response('OK')


# ---------------- ExamUserScore Routers -------------------- #

@router.get("/{exam_id}/process/", tags=["Exam"])
def process_exam(*, db: Session = Depends(get_db), exam_id):
    exam = crud.exam.get(db, id=exam_id)
    exam_status = db.scalars(select(ExamStatus).filter_by(type=ExamStatusType.TOTAL, exam=exam)).all()

    for item in exam.exam_lessons:

        stmt_delete = delete(ExamUserScore).where(ExamUserScore.exam_lesson == item)
        db.execute(stmt_delete)

        stmt_cte = select(ExamUserQuestion.exam_user_id, ExamUserQuestion.exam_question_id, ExamUserQuestion.score.label("user_score"),
                          ExamQuestion.exam_lesson_id,
                          ExamQuestion.score.label("question_score")).join(ExamQuestion).cte()

        stmt = select(stmt_cte.c.exam_user_id, stmt_cte.c.exam_lesson_id, func.sum(stmt_cte.c.user_score).label("user_score"),
                      func.sum(stmt_cte.c.question_score).label("question_score"), func.count().label("user_count_question")).group_by(
            stmt_cte.c.exam_user_id, stmt_cte.c.exam_lesson_id).where(stmt_cte.c.exam_lesson_id == item.id)

        for data in db.execute(stmt).all():
            data_dict = {
                'exam_user_id': data[0],
                'exam_lesson_id': data[1],
                'user_score': data[2],
                'question_score': data[3],
                'user_count_question': data[4]
            }

            if data_dict['user_count_question'] == len(item.exam_questions):
                if data_dict['user_score'] > data_dict['question_score']:
                    data_dict['user_score'] = data_dict['question_score']
                db_obj = ExamUserScore(
                    type=ExamScoreType.LESSON,
                    exam_lesson_id=data_dict['exam_lesson_id'],
                    exam_user_id=data_dict['exam_user_id'],
                    score=data_dict['user_score'],
                    score_percent=(data_dict['user_score'] / data_dict['question_score']) * 100
                )

                status = [status for status in exam_status if status.start_percent <= db_obj.score_percent < status.end_percent]
                db_obj.status = status[0] if len(status) > 0 else [status for status in exam_status if db_obj.score_percent == status.end_percent][0]

                db.add(db_obj)

    db.commit()
    return exam


# ---------------- Exam Report Routers -------------------- #

@router.get("/{exam_id}/report/{school_id}", tags=["Exam"])
def exam_report(*, db: Session = Depends(get_db), exam_id, school_id):
    users = db.scalars(select(User).join(ClassRoom).join(School).where(School.id == school_id)).all()
    exam = db.scalars(select(Exam).join(Grade).where(Exam.id == exam_id)).first()
    exam_status = db.scalars(select(ExamStatus).filter_by(type=ExamStatusType.TOTAL, exam=exam)).all()

    stmt_user_school = select(func.avg(ExamUserScore.score_percent)).join(ExamUser).join(User).join(ClassRoom).where(
        ClassRoom.school_id == school_id)
    user_school_avg = db.scalar(stmt_user_school)
    status_school = [status for status in exam_status if status.start_percent <= user_school_avg < status.end_percent]
    user_school_status = status_school[0].title if len(status_school) > 0 else \
        [status_school for status_school in exam_status if user_school_avg == status_school.end_percent][0].title

    for user in users:
        stmt_user_classroom = select(func.avg(ExamUserScore.score_percent)).join(ExamUser).join(User).where(User.classroom_id == user.classroom.id)
        user_classroom_avg = db.scalar(stmt_user_classroom)
        status_classroom = [status for status in exam_status if status.start_percent <= user_classroom_avg < status.end_percent]
        user_classroom_status = status_classroom[0].title if len(status_classroom) > 0 else \
            [status_classroom for status_classroom in exam_status if user_classroom_avg == status_classroom.end_percent][0].title

        stmt = select(ExamUser.id, ExamUser.exam_id, ExamUser.user_id,
                      Exam.title, Exam.start_datetime, Exam.duration,
                      User.first_name, User.last_name, User.username,
                      School.title.label("school_title"),
                      Agency.name.label("agency_title"),
                      ClassRoom.title.label("class_room_title")) \
            .join(Exam) \
            .join(User) \
            .join(Agency) \
            .join(ClassRoom).join(School) \
            .where(ExamUser.exam_id == exam_id).where(ExamUser.user_id == user.id)
        if db.execute(stmt).first():
            exam_user_dict = db.execute(stmt).first()._asdict()

            exam_user_scores = db.scalars(select(ExamUserScore).where(ExamUserScore.exam_user_id == exam_user_dict['id'])).all()
            for item in exam_user_scores:
                user_question = db.query(ExamUserQuestion) \
                    .join(ExamQuestion) \
                    .join(Topic) \
                    .order_by(ExamQuestion.question_number) \
                    .with_entities(ExamUserQuestion.score.label("score_user"),
                                   ExamQuestion.question_number,
                                   ExamQuestion.score.label("score_question"),
                                   Topic.id.label("topic_id"),
                                   Topic.title.label("topic_title")).where(
                    ExamUserQuestion.exam_user_id == exam_user_dict['id']) \
                    .where(ExamQuestion.exam_lesson == item.exam_lesson).all()
                list_questions_with_status = []

                for q in user_question:
                    q = q._asdict()
                    if q['score_user'] > q['score_question']:
                        q['score_user'] = q['score_question']
                    score_q_percent = (q['score_user'] / q['score_question']) * 100
                    q_item = {
                        'question_number': q['question_number'],
                        'topic_title': q['topic_title']
                    }
                    status = [status for status in exam_status if status.start_percent <= score_q_percent < status.end_percent]
                    q_item['status'] = status[0].title if len(status) > 0 else \
                        [status for status in exam_status if score_q_percent == status.end_percent][
                            0].title
                    list_questions_with_status.append(q_item)

                # user_question_qrouped = \
                #     db.query(ExamUserQuestion) \
                #         .join(ExamQuestion) \
                #         .join(Topic) \
                #         .group_by(Topic.title) \
                #         .with_entities(func.sum(ExamUserQuestion.score),
                #                        func.sum(ExamQuestion.score),
                #                        Topic.title.label("topic_title")).where(
                #         ExamUserQuestion.exam_user_id == exam_user_dict['id']) \
                #         .where(ExamQuestion.exam_lesson == item.exam_lesson).all()

                user_question_qrouped = \
                    db.execute(
                        select(func.sum(ExamUserQuestion.score).label("score_user"),
                               func.sum(ExamQuestion.score).label("score_question"),
                               Topic.title.label("topic_title")).select_from(ExamUserQuestion) \
                            .join(ExamQuestion) \
                            .join(Topic) \
                            .group_by(Topic.title) \
                            .where(
                            ExamUserQuestion.exam_user_id == exam_user_dict['id']) \
                            .where(ExamQuestion.exam_lesson == item.exam_lesson)
                    ).all()
                list_questions_topic_with_status = []

                for q in user_question_qrouped:
                    q = q._asdict()
                    if q['score_user'] > q['score_question']:
                        q['score_user'] = q['score_question']

                    score_q_percent = (q['score_user'] / q['score_question']) * 100
                    q_item = {
                        'topic_title': q['topic_title']
                    }
                    status = [status for status in exam_status if status.start_percent <= score_q_percent < status.end_percent]
                    q_item['status'] = status[0].title if len(status) > 0 else \
                        [status for status in exam_status if score_q_percent == status.end_percent][
                            0].title
                    list_questions_topic_with_status.append(q_item)

                yield {
                    'score_id': item.id,
                    'report_time': datetime.now(),
                    'exam': {
                        'title': exam.title,
                        'start_date_time': exam.start_datetime,
                        'grade_title': exam.grade.title + ' ' + exam.grade.base_grade.value
                    },
                    'user': {
                        'full_name': exam_user_dict['first_name'] + ' ' + exam_user_dict['last_name'],
                        'username': exam_user_dict['username'],
                    },
                    'school': {
                        'title': exam_user_dict['school_title']
                    },
                    'class_room': {
                        'title': exam_user_dict['class_room_title']
                    },
                    'agency': {
                        'title': exam_user_dict['agency_title']
                    },
                    'lesson': {
                        'title': item.exam_lesson.lesson.title,
                        'status': item.status.title,
                        "status_class_room": user_classroom_status,
                        "status_school": user_school_status,
                    },
                    'questions': list_questions_with_status,
                    'topics': list_questions_topic_with_status
                }


@router.get("/{exam_id}/schools/", tags=["Exam"])
def get_exam_schools(*, db: Session = Depends(get_db), exam_id):
    stmt_subquery = select(ExamUser.user_id).join(Exam).join(User).where(Exam.id == exam_id).subquery()

    stmt = select(User).join(ClassRoom).join(School).where(User.id.in_(stmt_subquery))

    aa = db.scalars(select(School).join(ClassRoom).join(User).where(User.id.in_(stmt_subquery)).distinct()).all()
    return aa
