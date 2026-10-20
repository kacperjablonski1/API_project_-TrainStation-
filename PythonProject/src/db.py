"""A module providing database access."""

import asyncio

import databases
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from asyncpg.exceptions import CannotConnectNowError,ConnectionDoesNotExistError

from src.config import config

metadata = sqlalchemy.MetaData()

user_table = sqlalchemy.Table(
    "user",
    metadata,
    sqlalchemy.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()")),
    sqlalchemy.Column('email', sqlalchemy.String, unique=True),
    sqlalchemy.Column('password', sqlalchemy.String),
)

trainStation_table = sqlalchemy.Table(
    "trainStation",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String, nullable=False),
    sqlalchemy.Column('city', sqlalchemy.String, nullable=False),
    sqlalchemy.Column('user_id', UUID(as_uuid=True), sqlalchemy.ForeignKey('user.id'), nullable=False),
)

train_table = sqlalchemy.Table(
    "train",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('number', sqlalchemy.String, nullable=False, unique=True),
    sqlalchemy.Column('name', sqlalchemy.String, nullable=True),
)

connection_table = sqlalchemy.Table(
    "connection", metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('train_id', sqlalchemy.Integer, sqlalchemy.ForeignKey("train.id"), nullable=False),
    sqlalchemy.Column('departure_station_id', sqlalchemy.Integer, sqlalchemy.ForeignKey("trainStation.id"), nullable=False),
    sqlalchemy.Column('arrival_station_id', sqlalchemy.Integer, sqlalchemy.ForeignKey("trainStation.id"), nullable=False),
    sqlalchemy.Column("departure_time", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("arrival_time", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("duration_minutes", sqlalchemy.Integer, nullable=False),
)

ticket_table = sqlalchemy.Table(
    "ticket",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('seat_type', sqlalchemy.String, nullable=False),
    sqlalchemy.Column('ticket_type', sqlalchemy.String, nullable=False),
    sqlalchemy.Column('price', sqlalchemy.Float, nullable=False),
    sqlalchemy.Column('passenger_name', sqlalchemy.String, nullable=False),
    sqlalchemy.Column('with_animal', sqlalchemy.Boolean, nullable=False, default=False),
    sqlalchemy.Column('with_disabled', sqlalchemy.Boolean, nullable=False, default=False),
    sqlalchemy.Column('user_id', UUID(as_uuid=True), sqlalchemy.ForeignKey("user.id"), nullable=False),
    sqlalchemy.Column('connection_id', sqlalchemy.Integer, sqlalchemy.ForeignKey("connection.id"), nullable=False),
)

wallet_table = sqlalchemy.Table(
    "wallet",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('balance', sqlalchemy.Float, nullable=False, default=0.0),
    sqlalchemy.Column('user_id', UUID(as_uuid=True), sqlalchemy.ForeignKey("user.id"), nullable=False, unique=True),
)

payment_table = sqlalchemy.Table(
    "payment",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('user_id', UUID(as_uuid=True), sqlalchemy.ForeignKey("user.id"), nullable=False),
    sqlalchemy.Column('ticket_id', sqlalchemy.Integer, sqlalchemy.ForeignKey("ticket.id"), nullable=False),
    sqlalchemy.Column('amount', sqlalchemy.Float, nullable=False, default=0.0),
    sqlalchemy.Column('method', sqlalchemy.String, nullable=False),
    sqlalchemy.Column('status', sqlalchemy.String, nullable=False),
)

db_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}/{config.DB_NAME}"
)

engine = create_async_engine(
    db_uri,
    echo=True,
    future=True,
    pool_pre_ping=True,
)

database = databases.Database(
    db_uri,
    force_rollback=False,
)


async def init_db(retries: int = 5, delay: int = 5) -> None:
    """Function initializing the DB.

    Args:
        retries (int, optional): Number of retries of connect to DB.
            Defaults to 5.
        delay (int, optional): Delay of connect do DB. Defaults to 2.
    """
    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all)
            return
        except (
            OperationalError,
            DatabaseError,
            CannotConnectNowError,
            ConnectionDoesNotExistError,
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to DB after several retries.")