"""Main module of the app"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from src.api.routers.user import router as user_router
from src.api.routers.ticket import router as ticket_router
from src.api.routers.wallet import router as wallet_router
from src.api.routers.payment import router as payment_router
from src.api.routers.train import router as train_router
from src.api.routers.trainStation import router as train_station_router
from src.api.routers.connection import router as connection_router

from src.container import Container
from src.db import database, init_db

container = Container()
container.wire(modules=[
    "src.api.routers.user",
    "src.api.routers.ticket",
    "src.api.routers.wallet",
    "src.api.routers.payment",
    "src.api.routers.train",
    "src.api.routers.trainStation",
    "src.api.routers.connection",
])


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


app.include_router(user_router, prefix="/users")
app.include_router(ticket_router, prefix="/tickets")
app.include_router(wallet_router, prefix="/wallet")
app.include_router(payment_router, prefix="/payments")
app.include_router(train_router, prefix="/trains")
app.include_router(train_station_router, prefix="/stations")
app.include_router(connection_router, prefix="/connections")



@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:
    """A function handling HTTP exceptions for logging purposes."""
    return await http_exception_handler(request, exception)
