import allure
import pytest

from pages.main_page import MainPage
from tests.marks import component, layer, owner, tm4j

pytestmark = [
    layer("web"),
    owner("goncharov"),
    component("хедер"),
    allure.epic("UI RuStore"),
    allure.feature("Хедер"),
]


@allure.tag("UI", "Хедер")
@allure.label("suite", "UI")
@allure.label("subSuite", "Хедер")
@tm4j("RUSTORE-UI-008")
@allure.id("RUSTORE-UI-008")
@allure.severity(allure.severity_level.NORMAL)
@allure.story("Навигация через логотип")
@allure.title("Логотип в хедере возвращает на главную страницу")
@pytest.mark.ui
@pytest.mark.regression
def test_header_logo_redirects_to_main_page():
    main_page = MainPage()

    with allure.step("Открыть страницу каталога"):
        main_page.open()
        main_page.go_to_instruction()

    with allure.step("Нажать на логотип в хедере"):
        main_page.click_logo()

    with allure.step("Проверить, что открылась главная страница RuStore"):
        main_page.should_have_correct_title()


@allure.tag("UI", "Хедер")
@allure.label("suite", "UI")
@allure.label("subSuite", "Хедер")
@tm4j("RUSTORE-UI-009")
@allure.id("RUSTORE-UI-009")
@allure.severity(allure.severity_level.NORMAL)
@allure.story("Пункты меню хедера")
@allure.title("Ссылки хедера имеют корректные href и target")
@pytest.mark.ui
@pytest.mark.regression
def test_header_links_have_expected_attrs():
    main_page = MainPage()

    with allure.step("Открыть главную страницу"):
        main_page.open()

    with allure.step("Проверить href у пунктов меню"):
        assert main_page.header_link_href("Приложения").endswith("/catalog")
        assert main_page.header_link_href("Игры").endswith("/catalog/games")
        assert main_page.header_link_href("Киоск").endswith("/kiosk")
        assert main_page.header_link_href("Блог").endswith("/prostore")
        assert main_page.header_link_href("Разработчикам").endswith("/developer")
        assert main_page.header_link_href("Помощь").endswith("/help")

    with allure.step("Проверить target у пунктов меню"):
        assert main_page.header_link_target("Приложения") == "_self"
        assert main_page.header_link_target("Игры") == "_self"
        assert main_page.header_link_target("Разработчикам") == "_blank"
        assert main_page.header_link_target("Помощь") == "_blank"


@allure.tag("UI", "Хедер")
@allure.label("suite", "UI")
@allure.label("subSuite", "Хедер")
@tm4j("RUSTORE-UI-010")
@allure.id("RUSTORE-UI-010")
@allure.severity(allure.severity_level.NORMAL)
@allure.story("Элементы хедера")
@allure.title("В хедере отображается кнопка поиска")
@pytest.mark.ui
@pytest.mark.regression
def test_header_has_search_button():
    main_page = MainPage()

    with allure.step("Открыть главную страницу"):
        main_page.open()

    with allure.step("Проверить наличие кнопки поиска"):
        main_page.should_have_search_button()
