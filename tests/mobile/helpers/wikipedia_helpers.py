import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait


def first_existing(driver, locators: list[tuple[str, str]]):
    for by, value in locators:
        try:
            return driver.find_element(by, value)
        except NoSuchElementException:
            continue
    return None


def tap_if_present(driver, locators: list[tuple[str, str]]) -> bool:
    element = first_existing(driver, locators)
    if element is None:
        return False
    element.click()
    return True


def prepare_wikipedia_home(driver) -> None:
    with allure.step("Закрыть onboarding/permission экраны, если отображаются"):
        tap_if_present(
            driver,
            [
                (AppiumBy.ID, "org.wikipedia:id/fragment_onboarding_skip_button"),
                (AppiumBy.ID, "org.wikipedia:id/fragment_onboarding_done_button"),
                (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button"),
                (AppiumBy.ID, "com.android.permissioncontroller:id/permission_deny_button"),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Not now")'),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Skip")'),
            ],
        )

    with allure.step("Дождаться главного экрана Wikipedia"):
        WebDriverWait(driver, 25).until(
            lambda d: (
                first_existing(
                    d,
                    [
                        (AppiumBy.ID, "org.wikipedia:id/search_container"),
                        (AppiumBy.ID, "org.wikipedia:id/main_toolbar_wordmark"),
                    ],
                )
                is not None
            )
        )


def open_search(driver) -> None:
    search_container = WebDriverWait(driver, 20).until(
        lambda d: first_existing(
            d,
            [
                (AppiumBy.ID, "org.wikipedia:id/search_container"),
                (AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"),
            ],
        )
    )
    assert search_container is not None
    search_container.click()


def search_input(driver):
    element = WebDriverWait(driver, 20).until(
        lambda d: first_existing(
            d,
            [
                (AppiumBy.ID, "org.wikipedia:id/search_src_text"),
                (
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().className("android.widget.EditText")',
                ),
            ],
        )
    )
    assert element is not None
    return element
