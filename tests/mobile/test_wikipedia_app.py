import allure
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait

from tests.marks import component, jira_issues, layer, microservice, owner, tm4j
from tests.mobile.helpers.wikipedia_helpers import (
    first_existing,
    open_search,
    prepare_wikipedia_home,
    search_input,
)

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
        prepare_wikipedia_home(mobile_driver)

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
        prepare_wikipedia_home(mobile_driver)

        with allure.step("Открыть поиск"):
            open_search(mobile_driver)

        with allure.step("Проверить, что поле ввода поиска отображается"):
            search_input(mobile_driver)

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
        prepare_wikipedia_home(mobile_driver)

        with allure.step("Открыть поиск и ввести запрос Appium"):
            open_search(mobile_driver)
            search_input_field = search_input(mobile_driver)
            search_input_field.send_keys("Appium")

        with allure.step("Проверить, что результаты поиска не пустые"):
            WebDriverWait(mobile_driver, 20).until(
                lambda d: (
                        first_existing(
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
        prepare_wikipedia_home(mobile_driver)

        with allure.step("Открыть поиск и ввести запрос Python"):
            open_search(mobile_driver)
            search_input(mobile_driver).send_keys("Python")

        with allure.step("Открыть первый результат поиска"):
            first_item = WebDriverWait(mobile_driver, 20).until(
                lambda d: first_existing(
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
                        first_existing(
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
        prepare_wikipedia_home(mobile_driver)

        with allure.step("Открыть поиск и ввести запрос"):
            open_search(mobile_driver)
            input_field = search_input(mobile_driver)
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
        prepare_wikipedia_home(mobile_driver)

        with allure.step("Открыть поиск и ввести невалидный запрос"):
            open_search(mobile_driver)
            search_input(mobile_driver).send_keys("asdkjashdkj123")

        with allure.step("Проверить отсутствие карточек результатов"):
            WebDriverWait(mobile_driver, 20).until(
                lambda d: (
                        first_existing(
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
                    first_existing(
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
        prepare_wikipedia_home(mobile_driver)

        with allure.step("Открыть экран поиска"):
            open_search(mobile_driver)
            search_input(mobile_driver)

        with allure.step("Нажать кнопку назад и проверить главный экран"):
            mobile_driver.back()
            WebDriverWait(mobile_driver, 20).until(
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
