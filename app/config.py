from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: str

    DB_HOST: str
    DB_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_DB: str

    @property
    def test_db_url(self):
        return f"postgresql+asyncpg://{self.TEST_POSTGRES_USER}:{self.TEST_POSTGRES_PASSWORD}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_POSTGRES_DB}"

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str

    SENTRY_DSN: str

    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
