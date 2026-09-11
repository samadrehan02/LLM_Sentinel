from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def create_engine(database_url: str) -> AsyncEngine:
    return create_async_engine(
        database_url,
        future=True,
    )


def create_session_factory(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def get_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


async def create_tables(
    engine: AsyncEngine,
) -> None:
    await engine.run_sync(
        Base.metadata.create_all,
    )


async def drop_tables(
    engine: AsyncEngine,
) -> None:
    await engine.run_sync(
        Base.metadata.drop_all,
    )


# Import models after Base is defined so that all ORM tables
# are registered with Base.metadata.
from sentinel.infrastructure import evaluation_model, event_model  # noqa: E402, F401