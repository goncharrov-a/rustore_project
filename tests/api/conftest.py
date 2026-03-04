import logging
from collections.abc import Generator

import pytest
import requests

from config.api_config import ApiSettings, load_api_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


@pytest.fixture(scope="session")
def api_settings() -> ApiSettings:
    return load_api_settings()


@pytest.fixture(scope="session")
def api_base_url(api_settings: ApiSettings) -> str:
    return api_settings.base_url


@pytest.fixture(scope="function")
def api_timeout(api_settings: ApiSettings) -> int:
    return api_settings.timeout


@pytest.fixture(scope="function")
def api_session(api_settings: ApiSettings) -> Generator[requests.Session, None, None]:
    session = requests.Session()
    session.headers.update(
        {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": api_settings.accept_language,
            "Content-Type": "application/json; charset=UTF-8",
            "User-Agent": api_settings.user_agent,
        }
    )
    session.base_url = api_settings.base_url  # type: ignore[attr-defined]
    yield session
    session.close()
