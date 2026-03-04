import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class ApiSettings:
    base_url: str
    timeout: int
    retries: int
    retry_delay_seconds: float
    accept_language: str
    user_agent: str


def load_api_settings() -> ApiSettings:
    load_dotenv(".env", override=False)

    return ApiSettings(
        base_url=os.getenv("API_BASE_URL", "https://fakestoreapi.com"),
        timeout=int(os.getenv("API_TIMEOUT", "15")),
        retries=int(os.getenv("API_RETRIES", "2")),
        retry_delay_seconds=float(os.getenv("API_RETRY_DELAY_SECONDS", "1.0")),
        accept_language=os.getenv("API_ACCEPT_LANGUAGE", "en-US,en;q=0.9"),
        user_agent=os.getenv(
            "API_USER_AGENT",
            (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
        ),
    )
