from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config.base import settings
from app.routers import education_system, lesson

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


app.include_router(education_system.router, tags=['Education System'])
app.include_router(lesson.router_lesson_parent, tags=['Lesson Parent'])
app.include_router(lesson.router_lesson, tags=['Lesson'])
