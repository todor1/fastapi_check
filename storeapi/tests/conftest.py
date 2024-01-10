import os
from typing import AsyncGenerator, Generator

import pytest

# allows to interact with the API without starting the server
from fastapi.testclient import TestClient
from httpx import AsyncClient  # ## allows to make requests to the API

os.environ["ENV_STATE"] = "test"

# from storeapi.routers.post import comment_table, post_table  # noqa: E402
from storeapi.database import database  # noqa: E402
from storeapi.main import app  # noqa: E402


@pytest.fixture(scope="session")
def anyio_backend() -> Generator:
    """
    telling fastapi to use the built-in asyncio framework
    as an async platform/backend when using async functions
    """
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    """just a function and not a fixture"""
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    """
    autouse=True means that this fixture will be used by all the tests in the module
    """
    await database.connect()
    yield
    await database.disconnect()


# @pytest.fixture(autouse=True)
# async def db() -> AsyncGenerator:
#     """
#     autouse=True means that this fixture will be used by all the tests in the module
#     """
#     post_table.clear()
#     comment_table.clear()
#     yield


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac
