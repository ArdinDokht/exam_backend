from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.base import settings
from app.routers import education_system, lesson, question, exam, auth, users

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(education_system.router, prefix="/grades", tags=['Education System'])
app.include_router(lesson.router, prefix="/lessons", tags=['Lesson'])
app.include_router(question.router, prefix="/questions", tags=['Question'])
app.include_router(exam.router, prefix="/exam")
app.include_router(auth.router, prefix="/auth", tags=['auth'])
app.include_router(users.router, prefix="/users", tags=['User'])

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=9000)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
    # expose_headers=["Set-Cookie"]
)
