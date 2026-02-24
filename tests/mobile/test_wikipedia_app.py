import allure
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

from tests.marks import component, jira_issues, layer, microservice, owner, tm4j

pytestmark = [
    layer("mobile"),
    owner("goncharov"),
    component("wikipedia-app"),
    microservice("Wikipedia Mobile"),
    allure.label("suite", "MOBILE"),
    allure.label("subSuite", "Wikipedia"),
    allure.epic("Mobile RuStore Diploma"),
    allure.feature("Wikipedia App"),
]


def _first_existing(driver, locators: list[tuple[str, str]]):
    for by, value in locators:
        try:
            return driver.find_element(by, value)
        except NoSuchElementException:
            continue
    return None


def _tap_if_present(driver, locators: list[tuple[str, str]]) -> bool:
    element = _first_existing(driver, locators)
    if element is None:
        return False
    element.click()
    return True


def _prepare_wikipedia_home(driver):
    with allure.step("Закрыть onboarding/permission экраны, если отображаются"):
        _tap_if_present(
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
                _first_existing(
                    d,
                    [
                        (AppiumBy.ID, "org.wikipedia:id/search_container"),
                        (AppiumBy.ID, "org.wikipedia:id/main_toolbar_wordmark"),
                    ],
                )
                is not None
            )
        )


def _open_search(driver):
    search_container = WebDriverWait(driver, 20).until(
        lambda d: _first_existing(
            d,
            [
                (AppiumBy.ID, "org.wikipedia:id/search_container"),
                (AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"),
            ],
        )
    )
    assert search_container is not None
    search_container.click()


def _search_input(driver):
    element = WebDriverWait(driver, 20).until(
        lambda d: _first_existing(
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


class TestWikipediaApp:
    @allure.tag("MOBILE", "Wikipedia", "Smoke")
    @allure.story("Запуск приложения")
    @allure.title("Wikipedia открывается и показывает главный экран")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.id("WIKI-MOB-001")
    @tm4j("WIKI-MOB-001")
    @jira_issues("DIP-MOB-201")
    @pytest.mark.mobile
    @pytest.mark.smoke
    def test_wikipedia_app_opens(self, mobile_driver):
        _prepare_wikipedia_home(mobile_driver)

        with allure.step("Проверить package приложения"):
            assert mobile_driver.current_package == "org.wikipedia"

    @allure.tag("MOBILE", "Wikipedia")
    @allure.story("Открытие поиска")
    @allure.title("Поиск Wikipedia открывается из главного экрана")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.id("WIKI-MOB-002")
    @tm4j("WIKI-MOB-002")
    @jira_issues("DIP-MOB-202")
    @pytest.mark.mobile
    @pytest.mark.regression
    def test_open_search_screen(self, mobile_driver):
        _prepare_wikipedia_home(mobile_driver)

        with allure.step("Открыть поиск"):
            _open_search(mobile_driver)

        with allure.step("Проверить, что поле ввода поиска отображается"):
            _search_input(mobile_driver)

    @allure.tag("MOBILE", "Wikipedia")
    @allure.story("Поиск статьи")
    @allure.title("Поиск по запросу Appium возвращает результаты")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.id("WIKI-MOB-003")
    @tm4j("WIKI-MOB-003")
    @jira_issues("DIP-MOB-203")
    @pytest.mark.mobile
    @pytest.mark.regression
    def test_search_returns_results(self, mobile_driver):
        _prepare_wikipedia_home(mobile_driver)

        with allure.step("Открыть поиск и ввести запрос Appium"):
            _open_search(mobile_driver)
            search_input = _search_input(mobile_driver)
            search_input.send_keys("Appium")

        with allure.step("Проверить, что результаты поиска не пустые"):
            WebDriverWait(mobile_driver, 20).until(
                lambda d: (
                    _first_existing(
                        d,
                        [
                            (AppiumBy.ID, "org.wikipedia:id/page_list_item_title"),
                            (AppiumBy.ID, "org.wikipedia:id/search_results_list"),
                        ],
                    )
                    is not None
                )
            )

    @allure.tag("MOBILE", "Wikipedia")
    @allure.story("Открытие статьи из поиска")
    @allure.title("Открытие первого результата поиска ведет на экран статьи")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.id("WIKI-MOB-004")
    @tm4j("WIKI-MOB-004")
    @jira_issues("DIP-MOB-204")
    @pytest.mark.mobile
    @pytest.mark.regression
    def test_open_first_search_result(self, mobile_driver):
        _prepare_wikipedia_home(mobile_driver)

        with allure.step("Открыть поиск и ввести запрос Python"):
            _open_search(mobile_driver)
            _search_input(mobile_driver).send_keys("Python")

        with allure.step("Открыть первый результат поиска"):
            first_item = WebDriverWait(mobile_driver, 20).until(
                lambda d: _first_existing(
                    d,
                    [
                        (AppiumBy.ID, "org.wikipedia:id/page_list_item_title"),
                        (AppiumBy.ID, "org.wikipedia:id/search_results_list"),
                    ],
                )
            )
            assert first_item is not None
            first_item.click()

        with allure.step("Проверить открытие экрана статьи"):
            WebDriverWait(mobile_driver, 20).until(
                lambda d: (
                    _first_existing(
                        d,
                        [
                            (AppiumBy.ID, "org.wikipedia:id/view_page_title_text"),
                            (AppiumBy.ID, "org.wikipedia:id/page_toolbar"),
                        ],
                    )
                    is not None
                )
            )

    @allure.tag("MOBILE", "Wikipedia")
    @allure.story("Очистка поля поиска")
    @allure.title("Поле поиска можно очистить после ввода запроса")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.id("WIKI-MOB-005")
    @tm4j("WIKI-MOB-005")
    @jira_issues("DIP-MOB-205")
    @pytest.mark.mobile
    @pytest.mark.regression
    def test_clear_search_input(self, mobile_driver):
        _prepare_wikipedia_home(mobile_driver)

        with allure.step("Открыть поиск и ввести запрос"):
            _open_search(mobile_driver)
            input_field = _search_input(mobile_driver)
            input_field.send_keys("OpenAI")

        with allure.step("Очистить поле и проверить, что отображается плейсхолдер поиска"):
            input_field.clear()
            assert input_field.text in ("", "Search Wikipedia")

    @allure.tag("MOBILE", "Wikipedia")
    @allure.story("Негативный поиск")
    @allure.title("По невалидному запросу не показываются карточки результатов")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.id("WIKI-MOB-006")
    @tm4j("WIKI-MOB-006")
    @jira_issues("DIP-MOB-206")
    @pytest.mark.mobile
    @pytest.mark.regression
    def test_search_no_results(self, mobile_driver):
        _prepare_wikipedia_home(mobile_driver)

        with allure.step("Открыть поиск и ввести невалидный запрос"):
            _open_search(mobile_driver)
            _search_input(mobile_driver).send_keys("asdkjashdkj123")

        with allure.step("Проверить отсутствие карточек результатов"):
            WebDriverWait(mobile_driver, 20).until(
                lambda d: (
                    _first_existing(
                        d,
                        [
                            (AppiumBy.ID, "org.wikipedia:id/search_results_list"),
                            (AppiumBy.ID, "org.wikipedia:id/search_empty_container"),
                            (AppiumBy.ID, "org.wikipedia:id/search_empty_message"),
                        ],
                    )
                    is not None
                )
            )
            assert (
                _first_existing(
                    mobile_driver, [(AppiumBy.ID, "org.wikipedia:id/page_list_item_title")]
                )
                is None
            )

    @allure.tag("MOBILE", "Wikipedia")
    @allure.story("Отмена поиска")
    @allure.title("Выход из поиска возвращает на главный экран")
    @allure.severity(allure.severity_level.MINOR)
    @allure.id("WIKI-MOB-007")
    @tm4j("WIKI-MOB-007")
    @jira_issues("DIP-MOB-207")
    @pytest.mark.mobile
    @pytest.mark.regression
    def test_back_from_search_returns_home(self, mobile_driver):
        _prepare_wikipedia_home(mobile_driver)

        with allure.step("Открыть экран поиска"):
            _open_search(mobile_driver)
            _search_input(mobile_driver)

        with allure.step("Нажать кнопку назад и проверить главный экран"):
            mobile_driver.back()
            WebDriverWait(mobile_driver, 20).until(
                lambda d: (
                    _first_existing(
                        d,
                        [
                            (AppiumBy.ID, "org.wikipedia:id/search_container"),
                            (AppiumBy.ID, "org.wikipedia:id/main_toolbar_wordmark"),
                        ],
                    )
                    is not None
                )
            )
