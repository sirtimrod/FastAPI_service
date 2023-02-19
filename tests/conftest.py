import asyncio
import os

# from datetime import timedelta
from typing import (
    Any,
    Generator,
    Final,
    Sequence,
)

import asyncpg
import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

import settings
from db.session import get_db
from main import app


_CLEAN_TABLES: Final[Sequence[str]] = ["users"]

_test_engine = create_async_engine(settings.TESTS_DATABASE_URL, future=True, echo=True)
_test_async_session = sessionmaker(_test_engine, expire_on_commit=True, class_=AsyncSession)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()  # TODO: understand how methods work
    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    os.system("alembic init migrations")
    os.system('alembic revision --autogenerate -m "test running migrations"')
    os.system("alembic upgrade heads")


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(settings.TESTS_DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=True, class_=AsyncSession)
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    async with async_session_test() as session:
        async with session.begin():
            for table in _CLEAN_TABLES:
                await session.execute(f"""TRUNCATE TABLE {table};""")


async def _get_test_db():
    try:
        yield _test_async_session()
    finally:
        pass


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(
        "".join(settings.TESTS_DATABASE_URL.split("+asyncpg"))
    )  # TODO: understand how method work
    yield pool
    await pool.close()


@pytest.fixture
async def get_user_from_database(asyncpg_pool):
    async def get_user_from_database_by_uuid(user_id: str):
        async with asyncpg_pool.acquire() as connection:  # TODO: understand how method work
            return await connection.fetch("""SELECT * FROM users WHERE user_id = $1;""", user_id)

    return get_user_from_database_by_uuid
