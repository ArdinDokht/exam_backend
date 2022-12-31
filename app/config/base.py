from typing import Union, List

from pydantic import BaseSettings, PostgresDsn, AnyHttpUrl, validator


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: PostgresDsn = 'postgresql://postgres:12345678@127.0.0.1:5432/exam'
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = ['https://exam-dashboard.chbk.run', 'https://exam-dashboard.chbk.run', 'http://localhost:3000',
                                              'https://localhost:3000',
                                              'http://192.168.1.3:3000', 'http://94.184.33.103:3000']

    SECRET_KEY: str = 'a1a726964889dd75b104265a97917e6ee917e54abe572d2948b226b4c9b3f2d2'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days
    JWT_ALGORITHM: str = 'HS256'

    class Config:
        case_sensitive = True


settings = Settings()
