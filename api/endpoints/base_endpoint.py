import json
import logging
import time
from typing import Any

import allure
import requests

from config.api_config import ApiSettings

logger = logging.getLogger(__name__)


class BaseEndpoint:
    def __init__(self, session: requests.Session, settings: ApiSettings):
        self.session = session
        self.base_url = str(getattr(session, "base_url", ""))
        self.timeout = settings.timeout
        self.retry_total = settings.retries
        self.retry_delay_seconds = settings.retry_delay_seconds
        self.retry_statuses = {403, 429, 500, 502, 503, 504}

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> requests.Response:
        method_upper = method.upper()
        url = self._build_url(endpoint)
        attempts = self._attempts_total(method_upper)
        response: requests.Response | None = None

        self._attach_request(method_upper, url, kwargs)

        for attempt in range(1, attempts + 1):
            try:
                response = self.session.request(
                    method=method_upper,
                    url=url,
                    timeout=self.timeout,
                    **kwargs,
                )
            except requests.RequestException as exc:
                if attempt == attempts:
                    raise
                self._log_request_exception(method_upper, url, attempt, attempts, exc)
                time.sleep(self.retry_delay_seconds)
                continue

            if self._should_retry(method_upper, response.status_code, attempt, attempts):
                self._log_retryable_status(
                    method_upper,
                    url,
                    response.status_code,
                    attempt,
                    attempts,
                )
                time.sleep(self.retry_delay_seconds)
                continue

            break

        if response is None:
            raise RuntimeError(f"request failed without response: {method_upper} {url}")

        logger.info(
            "status=%s | method=%s | url=%s",
            response.status_code,
            method_upper,
            url,
        )
        self._attach_response(response, attempt)

        return response

    def _build_url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"

    def _attempts_total(self, method: str) -> int:
        return self.retry_total + 1 if method == "GET" else 1

    def _attach_request(self, method: str, url: str, kwargs: dict[str, Any]) -> None:
        request_payload = {
            "method": method,
            "url": url,
            "params": kwargs.get("params"),
            "json": kwargs.get("json"),
            "headers": dict(self.session.headers),
        }
        allure.attach(
            json.dumps(request_payload, ensure_ascii=False, indent=2),
            name="request",
            attachment_type=allure.attachment_type.JSON,
        )

    def _attach_response(self, response: requests.Response, attempt: int) -> None:
        response_payload = {
            "status_code": response.status_code,
            "url": response.url,
            "headers": dict(response.headers),
            "body": self._safe_response_body(response),
            "attempts_used": attempt,
        }
        allure.attach(
            json.dumps(response_payload, ensure_ascii=False, indent=2),
            name="response",
            attachment_type=allure.attachment_type.JSON,
        )

    def _should_retry(self, method: str, status_code: int, attempt: int, attempts: int) -> bool:
        return method == "GET" and status_code in self.retry_statuses and attempt < attempts

    def _log_retryable_status(
        self,
        method: str,
        url: str,
        status_code: int,
        attempt: int,
        attempts: int,
    ) -> None:
        attempt_str = f"{attempt}/{attempts}"
        logger.warning(
            "retryable status=%s on attempt=%s | method=%s | url=%s",
            status_code,
            attempt_str,
            method,
            url,
        )

    def _log_request_exception(
        self,
        method: str,
        url: str,
        attempt: int,
        attempts: int,
        exc: requests.RequestException,
    ) -> None:
        attempt_str = f"{attempt}/{attempts}"
        logger.warning(
            "request error on attempt=%s | method=%s | url=%s | error=%s",
            attempt_str,
            method,
            url,
            exc,
        )

    @staticmethod
    def _safe_response_body(response: requests.Response):
        try:
            return response.json()
        except Exception:
            return response.text
