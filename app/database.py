from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.test_db_url
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.db_url
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
engine_nullpool = create_async_engine(DATABASE_URL, poolclass=NullPool)

session_pool = async_sessionmaker(engine, expire_on_commit=False)
async_session_maker_nullpool = async_sessionmaker(engine_nullpool, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
