import logging
import os
from collections.abc import Generator

import pytest
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


@pytest.fixture(scope="session")
def api_base_url() -> str:
    return os.getenv("API_BASE_URL", "https://fakestoreapi.com")


@pytest.fixture(scope="session")
def api_timeout() -> int:
    return int(os.getenv("API_TIMEOUT", "15"))


@pytest.fixture(scope="function")
def api_session(api_base_url: str) -> Generator[requests.Session, None, None]:
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json; charset=UTF-8"})
    session.base_url = api_base_url  # type: ignore[attr-defined]
    yield session
    session.close()
