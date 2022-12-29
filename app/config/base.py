from typing import Union, List

from pydantic import BaseSettings, PostgresDsn, AnyHttpUrl, validator


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: PostgresDsn = 'postgresql://postgres:12345678@127.0.0.1:5432/exam'
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = ['http://localhost:3000', 'http://192.168.1.3:3000', 'http://94.184.33.103:3000']

    # @validator("BACKEND_CORS_ORIGINS", pre=True)
    # def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
    #     if isinstance(v, str) and not v.startswith("["):
    #         return [i.strip() for i in v.split(",")]
    #     elif isinstance(v, (list, str)):
    #         return v
    #     raise ValueError(v)

    class Config:
        case_sensitive = True


settings = Settings()
