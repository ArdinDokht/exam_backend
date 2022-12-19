from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config.base import settings
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
async def root():
    return {"message": "Hello World"}


app.include_router(education_system.router, prefix="/grades", tags=['Education System'])
app.include_router(lesson.router, prefix="/lessons", tags=['Lesson'])
app.include_router(question.router, prefix="/questions", tags=['Question'])
app.include_router(exam.router, prefix="/exam", tags=['Exam'])
