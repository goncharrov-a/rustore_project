import json
import logging
import os
import time
from typing import Any

import allure
import requests

logger = logging.getLogger(__name__)


class BaseEndpoint:
    def __init__(self, session: requests.Session, timeout: int = 10):
        self.session = session
        self.base_url = str(getattr(session, "base_url", ""))
        self.timeout = timeout
        self.retry_total = int(os.getenv("API_RETRIES", "2"))
        self.retry_delay_seconds = float(os.getenv("API_RETRY_DELAY_SECONDS", "1.0"))
        self.retry_statuses = {403, 429, 500, 502, 503, 504}

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> requests.Response:
        url = f"{self.base_url}{endpoint}"

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

        method_upper = method.upper()
        attempts = self.retry_total + 1 if method_upper == "GET" else 1
        response: requests.Response | None = None

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
                logger.warning(
                    "request error on attempt=%s/%s | method=%s | url=%s | error=%s",
                    attempt,
                    attempts,
                    method_upper,
                    url,
                    exc,
                )
                time.sleep(self.retry_delay_seconds)
                continue

            if (
                method_upper == "GET"
                and response.status_code in self.retry_statuses
                and attempt < attempts
            ):
                logger.warning(
                    "retryable status=%s on attempt=%s/%s | method=%s | url=%s",
                    response.status_code,
                    attempt,
                    attempts,
                    method_upper,
                    url,
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

        return response

    @staticmethod
    def _safe_response_body(response: requests.Response):
        try:
            return response.json()
        except Exception:
            return response.text
