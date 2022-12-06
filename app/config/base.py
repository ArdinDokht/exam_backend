from pydantic import BaseSettings, PostgresDsn, AnyHttpUrl


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: PostgresDsn = 'postgresql://postgres:12345678@127.0.0.1:5432/exam'
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = ['http://localhost:3000']

    class Config:
        case_sensitive = True


settings = Settings()
