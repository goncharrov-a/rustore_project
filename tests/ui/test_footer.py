import allure
import pytest

from pages.footer import Footer
from pages.main_page import MainPage
from tests.marks import component, layer, owner, tm4j

pytestmark = [
    layer("web"),
    owner("goncharov"),
    component("футер"),
    allure.epic("UI RuStore"),
    allure.feature("Футер"),
]


@allure.tag("UI", "Футер")
@allure.label("suite", "UI")
@allure.label("subSuite", "Футер")
@tm4j("RUSTORE-UI-005")
@allure.id("RUSTORE-UI-005")
@allure.severity(allure.severity_level.NORMAL)
@allure.story("Контент футера")
@allure.title("В футере отображается QR-код для скачивания RuStore")
@pytest.mark.ui
@pytest.mark.footer
def test_footer_contains_qr_code():
    main_page = MainPage()
    footer = Footer()

    with allure.step("Открыть главную страницу"):
        main_page.open()

    with allure.step("Прокрутить страницу к футеру"):
        footer.scroll_to_footer()

    with allure.step("Проверить отображение QR-кода"):
        footer.should_have_qr_code()


@allure.tag("UI", "Футер")
@allure.label("suite", "UI")
@allure.label("subSuite", "Футер")
@tm4j("RUSTORE-UI-006")
@allure.id("RUSTORE-UI-006")
@allure.severity(allure.severity_level.NORMAL)
@allure.story("Контент футера")
@allure.title("В футере отображается кнопка обращения в поддержку")
@pytest.mark.ui
@pytest.mark.footer
def test_footer_contains_support_button():
    main_page = MainPage()
    footer = Footer()

    with allure.step("Открыть главную страницу"):
        main_page.open()

    with allure.step("Прокрутить страницу к футеру"):
        footer.scroll_to_footer()

    with allure.step("Проверить отображение кнопки обращения в поддержку"):
        footer.should_have_support_button()
