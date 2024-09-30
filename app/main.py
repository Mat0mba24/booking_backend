import time
from contextlib import asynccontextmanager

import sentry_sdk
import uvicorn
from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.importer.router import router as router_import
from app.logger import logger
from app.users.router import router_auth, router_users
from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis = aioredis.from_url(
        url=f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


if settings.MODE == "TEST":
    # При тестировании через pytest, необходимо подключать Redis, чтобы кэширование работало.
    # Иначе декоратор @cache из библиотеки fastapi-cache ломает выполнение кэшируемых эндпоинтов.
    # Из этого следует вывод, что сторонние решения порой ломают наш код, и это бывает проблематично поправить.
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
else:
    # Подключение Sentry для мониторинга ошибок. Лучше выключать на период локального тестирования
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
    )

app = FastAPI(
    title="Бронирование Отелей",
    lifespan=lifespan
)

prefix_router = APIRouter(prefix="/api")
for router in [
    # Включение основных роутеров
    router_auth,
    router_users,
    router_hotels,
    router_rooms,
    router_bookings,
    # Включение дополнительных роутеров
    router_images,
    router_import
]:
    prefix_router.include_router(router)

app.include_router(prefix_router)

# Подключение CORS, чтобы запросы к API могли приходить из браузера
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:3000",
#         "http://127.0.0.1:3000"
#     ],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
#     allow_headers=[
#         "Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
#         "Access-Control-Allow-Origin",
#         "Authorization"
#     ],
# )

# Подключение админки
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(BookingsAdmin)

app.mount("/static", StaticFiles(directory="app/static"), "static")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return response


uvicorn.run(
    app,
    host="0.0.0.0",
    port=8000,
    proxy_headers=True,
    forwarded_allow_ips="*"
)
