from contextlib import asynccontextmanager
from logging import INFO, basicConfig, getLogger
from typing import AsyncGenerator

from fastapi import FastAPI

from app.db.db_setup import create_db_and_tables
from app.routers import product, music, place, person, entity

logger = getLogger(__name__)
basicConfig(level=INFO)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting up...")
    create_db_and_tables()
    yield
    logger.info("Shutting down...")
    logger.info("Finished shutting down.")


def get_app() -> FastAPI:
    app = FastAPI(title="FastAPI Snd", lifespan=lifespan)
    app.include_router(product.router)
    app.include_router(music.router)
    app.include_router(place.router)
    app.include_router(person.router)
    app.include_router(entity.router)
    return app


app = get_app()
