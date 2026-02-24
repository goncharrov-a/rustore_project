import allure
import pytest

from pages.main_page import MainPage
from tests.marks import component, layer, owner, tm4j

pytestmark = [
    layer("web"),
    owner("goncharov"),
    component("главная-страница"),
    allure.epic("UI RuStore"),
    allure.feature("Главная страница"),
]


@allure.tag("UI", "Смоук")
@allure.label("suite", "UI")
@allure.label("subSuite", "Главная")
@tm4j("RUSTORE-UI-001")
@allure.id("RUSTORE-UI-001")
@allure.severity(allure.severity_level.CRITICAL)
@allure.story("Открытие главной страницы")
@allure.title("Главная страница RuStore открывается и содержит основные элементы")
@pytest.mark.ui
@pytest.mark.smoke
def test_main_page_open_and_base_elements_present():
    main_page = MainPage()

    with allure.step("Открыть главную страницу RuStore"):
        main_page.open()

    with allure.step("Проверить заголовок страницы"):
        main_page.should_have_correct_title()

    with allure.step("Проверить наличие и кликабельность логотипа"):
        main_page.should_have_clickable_logo()

    with allure.step("Проверить наличие кнопки «Скачать RuStore»"):
        main_page.should_have_download_button()
