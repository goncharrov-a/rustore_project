import allure
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from config.mobile_config import MobileRemoteConfig, load_mobile_settings


@pytest.fixture(scope="function")
def mobile_driver():
    settings = load_mobile_settings()
    config = settings.config

    capabilities = config.model_dump(by_alias=True, exclude={"appium_server_url"})

    if isinstance(config, MobileRemoteConfig):
        capabilities.update(
            {
                "bstack:options": {
                    "userName": config.bstack_user_name,
                    "accessKey": config.bstack_access_key,
                    "projectName": config.project_name,
                    "buildName": config.build_name,
                    "sessionName": config.session_name,
                }
            }
        )

    options = UiAutomator2Options().load_capabilities(capabilities)
    appium_server_url = str(config.appium_server_url)  # type: ignore[attr-defined]
    driver = webdriver.Remote(appium_server_url, options=options)

    yield driver

    allure.attach(
        driver.get_screenshot_as_png(),
        name="mobile_screenshot",
        attachment_type=allure.attachment_type.PNG,
    )
    allure.attach(
        driver.page_source,
        name="mobile_page_source",
        attachment_type=allure.attachment_type.XML,
    )

    if settings.env == "remote":
        video_url = (
            f"https://app-automate.browserstack.com/dashboard/v2/sessions/{driver.session_id}"
        )
        allure.attach(
            video_url,
            name="mobile_video_url",
            attachment_type=allure.attachment_type.URI_LIST,
        )

    driver.quit()
