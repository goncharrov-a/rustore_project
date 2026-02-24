import json
import logging
from typing import Any

import allure
import requests

logger = logging.getLogger(__name__)


class BaseEndpoint:
    def __init__(self, session: requests.Session, timeout: int = 10):
        self.session = session
        self.base_url = str(getattr(session, "base_url", ""))
        self.timeout = timeout

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

        response = self.session.request(method=method, url=url, timeout=self.timeout, **kwargs)

        logger.info(
            "status=%s | method=%s | url=%s",
            response.status_code,
            method,
            url,
        )

        response_payload = {
            "status_code": response.status_code,
            "url": response.url,
            "headers": dict(response.headers),
            "body": self._safe_response_body(response),
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
