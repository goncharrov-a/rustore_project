import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WIKI_APK = PROJECT_ROOT / "resources" / "apk" / "wikipedia.apk"


class MobileBaseConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    platform_name: str = Field("Android", alias="platformName")
    automation_name: str = Field("UiAutomator2", alias="automationName")
    app_package: str = Field("org.wikipedia", alias="appPackage")
    app_activity: str = Field("org.wikipedia.main.MainActivity", alias="appActivity")
    app_wait_activity: str = Field("*", alias="appWaitActivity")
    language: str = "en"
    locale: str = "US"
    new_command_timeout: int = Field(120, alias="newCommandTimeout")


class MobileLocalConfig(MobileBaseConfig):
    appium_server_url: str = "http://127.0.0.1:4723"
    device_name: str = Field("Android Emulator", alias="deviceName")
    app: str = str(DEFAULT_WIKI_APK)


class MobileRemoteConfig(MobileBaseConfig):
    appium_server_url: str = "http://hub.browserstack.com/wd/hub"
    device_name: str = Field("Google Pixel 7", alias="deviceName")
    bstack_user_name: str = Field(alias="bstack_userName")
    bstack_access_key: str = Field(alias="bstack_accessKey")
    project_name: str = Field("Diploma Mobile", alias="projectName")
    build_name: str = Field("Wikipedia build", alias="buildName")
    session_name: str = Field("Wikipedia tests", alias="sessionName")
    app: str = ""


@dataclass
class MobileSettings:
    env: str
    config: MobileBaseConfig


def load_mobile_settings() -> MobileSettings:
    env = os.getenv("MOBILE_ENV", "local").lower()
    config: MobileBaseConfig

    if env == "remote":
        load_dotenv(".env.mobile.remote", override=False)
        config = MobileRemoteConfig.model_validate(
            {
                "bstack_userName": os.getenv("BROWSERSTACK_USER", ""),
                "bstack_accessKey": os.getenv("BROWSERSTACK_KEY", ""),
                "deviceName": os.getenv("MOBILE_DEVICE", "Google Pixel 7"),
                "app": os.getenv("BROWSERSTACK_APP", ""),
                "appPackage": os.getenv("MOBILE_APP_PACKAGE", "org.wikipedia"),
                "appActivity": os.getenv(
                    "MOBILE_APP_ACTIVITY",
                    "org.wikipedia.main.MainActivity",
                ),
            }
        )
    else:
        load_dotenv(".env.mobile.local", override=False)
        config = MobileLocalConfig.model_validate(
            {
                "appium_server_url": os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723"),
                "deviceName": os.getenv("MOBILE_DEVICE", "emulator-5554"),
                "app": os.getenv("MOBILE_APP_PATH", str(DEFAULT_WIKI_APK)),
                "appPackage": os.getenv("MOBILE_APP_PACKAGE", "org.wikipedia"),
                "appActivity": os.getenv(
                    "MOBILE_APP_ACTIVITY",
                    "org.wikipedia.main.MainActivity",
                ),
            }
        )

    return MobileSettings(env=env, config=config)
