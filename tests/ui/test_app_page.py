import allure
import pytest

from pages.app_page import AppPage
from tests.marks import component, layer, owner, tm4j

pytestmark = [
    layer("web"),
    owner("goncharov"),
    component("карточка-приложения"),
    allure.epic("UI RuStore"),
    allure.feature("Карточка приложения"),
]


@allure.tag("UI", "Карточка приложения")
@allure.label("suite", "UI")
@allure.label("subSuite", "Карточка приложения")
@tm4j("RUSTORE-UI-007")
@allure.id("RUSTORE-UI-007")
@allure.severity(allure.severity_level.CRITICAL)
@allure.story("Просмотр карточки приложения")
@allure.title("Карточка приложения Госуслуги отображает основную информацию")
@pytest.mark.ui
@pytest.mark.card
def test_app_page_gosuslugi_title_name_and_buttons():
    page = AppPage()

    with allure.step("Открыть страницу приложения «Госуслуги»"):
        page.open("/catalog/app/ru.rostel")

    with allure.step("Проверить загрузку основной информации страницы"):
        page.should_be_loaded()

    with allure.step("Проверить заголовок страницы"):
        page.should_have_title("Госуслуги — скачать для Android 4,5★ бесплатно 📱 в RuStore")

    with allure.step("Проверить название приложения"):
        page.should_have_name("Госуслуги")

    with allure.step("Проверить наличие кнопок установки и открытия QR-кода"):
        page.should_have_action_buttons()
