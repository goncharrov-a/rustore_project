import json
import os
from urllib.parse import urlsplit, urlunsplit

import allure
import pytest

# Compatibility shim:
# selene==2.0.0rc9 imports AnyDevice from selenium.action_chains,
# but recent selenium versions do not export this alias.
import selenium.webdriver.common.action_chains as _action_chains
from dotenv import load_dotenv

if not hasattr(_action_chains, "AnyDevice"):
    _action_chains.AnyDevice = object  # type: ignore[attr-defined]

from selene import browser
from selenium import webdriver


def _build_remote_url() -> str:
    explicit = os.getenv("SELENOID_URL", "").strip()
    if explicit.startswith("http://") or explicit.startswith("https://"):
        return explicit

    login = os.getenv("SELENOID_LOGIN", "").strip()
    password = os.getenv("SELENOID_PASS", "").strip()
    host = explicit
    if host and login and password:
        return f"https://{login}:{password}@{host}/wd/hub"
    if host:
        return f"https://{host}/wd/hub"
    return ""


def _build_video_public_base(remote_url: str) -> str:
    explicit = os.getenv("SELENOID_UI", "").strip()
    if explicit:
        return explicit.rstrip("/")

    parsed = urlsplit(remote_url)
    if not parsed.scheme or not parsed.hostname:
        return ""

    host = f"{parsed.scheme}://{parsed.hostname}"
    if parsed.port:
        host = f"{host}:{parsed.port}"
    return host.rstrip("/")


def _build_auth_video_url(public_url: str, remote_url: str) -> str:
    remote = urlsplit(remote_url)
    if not remote.username:
        return public_url

    auth = remote.username
    if remote.password:
        auth = f"{auth}:{remote.password}"

    parts = urlsplit(public_url)
    return urlunsplit(
        (
            parts.scheme,
            f"{auth}@{parts.netloc}",
            parts.path,
            parts.query,
            parts.fragment,
        )
    )


def _attach_selenoid_video(session_id: str, remote_url: str) -> None:
    base = _build_video_public_base(remote_url)
    if not base:
        return

    public_video_url = f"{base}/video/{session_id}.mp4"
    auth_video_url = _build_auth_video_url(public_video_url, remote_url)

    html = (
        "<html><body><video width='100%' height='100%' controls autoplay>"
        f"<source src='{auth_video_url}' type='video/mp4'></video>"
        "</body></html>"
    )
    allure.attach(
        html,
        name=f"video_{session_id}",
        attachment_type=allure.attachment_type.HTML,
    )
    allure.attach(
        public_video_url,
        name="video_url",
        attachment_type=allure.attachment_type.URI_LIST,
    )


@pytest.fixture(scope="function", autouse=True)
def ui_browser_setup():
    # Jenkins freestyle often writes variables to ".env" in workspace.
    # Load it explicitly so SELENOID_* and other vars are available for the test run.
    load_dotenv('.env', override=True)

    base_url = os.getenv("UI_BASE_URL", "https://www.rustore.ru")
    browser_name = os.getenv("UI_BROWSER", "chrome")
    width = int(os.getenv("UI_BROWSER_WIDTH", "1920"))
    height = int(os.getenv("UI_BROWSER_HEIGHT", "1080"))
    remote_url = _build_remote_url()

    browser.config.base_url = base_url
    browser.config.window_width = width
    browser.config.window_height = height
    browser.config.timeout = float(os.getenv("UI_TIMEOUT", "10"))

    if remote_url:
        options = (
            webdriver.ChromeOptions() if browser_name == "chrome" else webdriver.FirefoxOptions()
        )
        options.set_capability("selenoid:options", {"enableVNC": True, "enableVideo": True})
        browser.config.driver = webdriver.Remote(command_executor=remote_url, options=options)
    else:
        browser.config.browser_name = browser_name  # type: ignore[attr-defined]

    yield

    executor = browser.config._executor
    if executor.is_driver_set:
        driver = executor.driver_instance
        allure.attach(
            driver.get_screenshot_as_png(),
            name='screenshot',
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(
            driver.page_source,
            name='page_source',
            attachment_type=allure.attachment_type.HTML,
        )

        try:
            get_log = getattr(driver, 'get_log', None)
            if callable(get_log):
                logs = get_log('browser')
                allure.attach(
                    json.dumps(logs, indent=2, ensure_ascii=False),
                    name='browser_logs',
                    attachment_type=allure.attachment_type.JSON,
                )
        except Exception:
            pass

        session_id = getattr(driver, 'session_id', None)
        if session_id and remote_url:
            _attach_selenoid_video(session_id, remote_url)

        driver.quit()
