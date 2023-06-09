from typing import Union, List

from pydantic import BaseSettings, PostgresDsn, AnyHttpUrl, validator


class Settings(BaseSettings):
    # SQLALCHEMY_DATABASE_URL: PostgresDsn = 'postgresql://cldmp8abp000l9gmp3hbk0qkq:ulO7W5iD5FvLMJqhVKaOJrW8@192.168.110.52:9000/exam'
    SQLALCHEMY_DATABASE_URL: PostgresDsn = 'postgresql://postgres:12345678@127.0.0.1:5432/exam'
    # SQLALCHEMY_DATABASE_URL: PostgresDsn = 'postgresql://cleaz41op0009ahtt9zy5519q:2I9Vq8HDZyF2mGrfl8dUkSnp@192.168.233.230:9000/exam'
    # SQLALCHEMY_DATABASE_URL: PostgresDsn = 'postgresql://postgres:w4KXGj3ejxbCmVhU@services.irn2.chabokan.net:54933/exam'

    # COOKIE_DOMAIN: str = '.testcraft.ir'
    COOKIE_DOMAIN: str = '127.0.0.1'
    # COOKIE_DOMAIN: str = '.chbk.run'
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = ['https://exam-dashboard.chbk.run', 'https://exam-dashboard.chbk.run', 'http://localhost:3000',
                                              'https://localhost:3000',
                                              'http://192.168.1.3:3000', 'http://94.184.33.103:3000', 'http://0.0.0.0:3000', 'http://127.0.0.1:3000',
                                              'https://motrobus.ir', 'https://testcraft.ir']

    SECRET_KEY: str = 'a1a726964889dd75b104265a97917e6ee917e54abe572d2948b226b4c9b3f2d2'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days
    JWT_ALGORITHM: str = 'HS256'

    class Config:
        case_sensitive = True


settings = Settings()
