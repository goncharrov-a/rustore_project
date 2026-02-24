import json
import os

import allure
import pytest

# Compatibility shim:
# selene==2.0.0rc9 imports AnyDevice from selenium.action_chains,
# but recent selenium versions do not export this alias.
import selenium.webdriver.common.action_chains as _action_chains

if not hasattr(_action_chains, "AnyDevice"):
    _action_chains.AnyDevice = object  # type: ignore[attr-defined]

from selene import browser
from selenium import webdriver


@pytest.fixture(scope="function", autouse=True)
def ui_browser_setup():
    base_url = os.getenv("UI_BASE_URL", "https://www.rustore.ru")
    browser_name = os.getenv("UI_BROWSER", "chrome")
    width = int(os.getenv("UI_BROWSER_WIDTH", "1920"))
    height = int(os.getenv("UI_BROWSER_HEIGHT", "1080"))
    selenoid_url = os.getenv("SELENOID_URL")

    browser.config.base_url = base_url
    browser.config.window_width = width
    browser.config.window_height = height
    browser.config.timeout = float(os.getenv("UI_TIMEOUT", "10"))

    if selenoid_url:
        options = (
            webdriver.ChromeOptions() if browser_name == "chrome" else webdriver.FirefoxOptions()
        )
        options.set_capability("selenoid:options", {"enableVNC": True, "enableVideo": True})
        browser.config.driver = webdriver.Remote(command_executor=selenoid_url, options=options)
    else:
        browser.config.browser_name = browser_name  # type: ignore[attr-defined]

    yield

    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name="screenshot",
        attachment_type=allure.attachment_type.PNG,
    )
    allure.attach(
        browser.driver.page_source,
        name="page_source",
        attachment_type=allure.attachment_type.HTML,
    )

    try:
        get_log = getattr(browser.driver, "get_log", None)
        if callable(get_log):
            logs = get_log("browser")
            allure.attach(
                json.dumps(logs, indent=2, ensure_ascii=False),
                name="browser_logs",
                attachment_type=allure.attachment_type.JSON,
            )
    except Exception:
        pass

    session_id = getattr(browser.driver, "session_id", None)
    if session_id and selenoid_url:
        host = selenoid_url.replace("wd/hub", "")
        video_url = f"{host}video/{session_id}.mp4"
        allure.attach(video_url, name="video_url", attachment_type=allure.attachment_type.URI_LIST)

    browser.quit()
