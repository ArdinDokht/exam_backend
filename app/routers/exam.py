from datetime import datetime
from urllib import request

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select, func, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, aliased

from app import schemas, crud, enums
from app.dependencies import get_db
from app.enums import ExamStatusType, ExamScoreType
from app.models import Exam, User, Grade, Agency, ClassRoom, School, Topic
from app.models.exam import ExamQuestion, ExamLesson, ExamUser, ExamUserQuestion, ExamStatus, ExamUserScore

router = APIRouter()


# ---------------- Exam Routers -------------------- #

@router.post("/", response_model=schemas.Exam, tags=["Exam"])
def create_exam(*, db: Session = Depends(get_db), exam_in: schemas.ExamCreate):
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
def get_all_exams(*, db: Session = Depends(get_db)):
    exams = crud.exam.get_all(db)
    return exams


@router.get("/{exam_id}", response_model=schemas.Exam, tags=["Exam"])
def get_exam(*, db: Session = Depends(get_db), exam_id):
    exam = crud.exam.get(db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam


@router.put("/{exam_id}", response_model=schemas.Exam, tags=["Exam"])
def update_exam(*, db: Session = Depends(get_db), exam_id, exam_in: schemas.ExamUpdate):
    exam = crud.exam.get(db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    exam = crud.exam.update(db, db_obj=exam, obj_in=exam_in)
    return exam


# ---------------- ExamQuestion Routers -------------------- #


@router.get("/{exam_id}/questions/", response_model=list[schemas.ExamQuestion], tags=["ExamQuestion"])
def get_exam_questions(*, db: Session = Depends(get_db), exam_id):
    exam = crud.exam.get(db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return db.scalars(select(ExamQuestion).join(ExamLesson).join(Exam).where(Exam.id == exam_id)).all()


@router.put("/{exam_id}/questions/{exam_question_id}/advance/", tags=["ExamQuestion"], response_model=schemas.ExamQuestion)
def update_exam_question_advance(*, db: Session = Depends(get_db), exam_question_id, exam_id, exam_question_in: schemas.ExamQuestionAdvanceUpdate):
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
        db_obj = ExamLesson(exam_id=exam.id, lesson_id=exam_question_in.lesson_id, coefficient=0, type=enums.ExamLessonType.GENERAL, duration=0)
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
def create_exam_question_advance(*, db: Session = Depends(get_db), exam_id, exam_question_in: schemas.ExamQuestionAdvanceCreate):
    exam = crud.exam.get(db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    exam_lesson = db.execute(
        select(ExamLesson)
        .where(ExamLesson.exam_id == exam_id).where(ExamLesson.lesson_id == exam_question_in.lesson_id)
    ).scalar()

    if exam_lesson is None:
        db_obj = ExamLesson(exam_id=exam.id, lesson_id=exam_question_in.lesson_id, coefficient=0, type=enums.ExamLessonType.GENERAL, duration=0)
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
