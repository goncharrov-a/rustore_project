import allure
import pytest

from pages.main_page import MainPage
from pages.search_page import SearchPage
from pages.search_results_page import SearchResultsPage
from tests.marks import component, layer, owner, tm4j

pytestmark = [
    layer("web"),
    owner("goncharov"),
    component("поиск"),
    allure.epic("UI RuStore"),
    allure.feature("Поиск"),
]


@allure.tag("UI", "Поиск")
@allure.label("suite", "UI")
@allure.label("subSuite", "Поиск")
@tm4j("RUSTORE-UI-003")
@allure.id("RUSTORE-UI-003")
@allure.severity(allure.severity_level.NORMAL)
@allure.story("Открытие формы поиска")
@allure.title("Страница поиска открывается и отображает список «Часто ищут»")
@pytest.mark.ui
@pytest.mark.search
def test_search_page_opens_and_shows_trends():
    main = MainPage()
    search = SearchPage()

    with allure.step("Открыть главную страницу"):
        main.open()

    with allure.step("Открыть поиск из шапки сайта"):
        main.open_search()

    with allure.step("Проверить, что открылась страница поиска"):
        search.should_be_opened()

    with allure.step("Проверить, что поле поиска пустое и плейсхолдер корректный"):
        search.should_have_empty_input_and_placeholder()

    with allure.step("Проверить, что список «Часто ищут» не пустой"):
        search.should_have_non_empty_trends()


@allure.tag("UI", "Поиск")
@allure.label("suite", "UI")
@allure.label("subSuite", "Поиск")
@tm4j("RUSTORE-UI-004")
@allure.id("RUSTORE-UI-004")
@allure.severity(allure.severity_level.CRITICAL)
@allure.story("Получение результатов поиска")
@allure.title("Поиск по запросу «Госуслуги» возвращает результаты")
@pytest.mark.ui
@pytest.mark.search
def test_search_shows_results():
    main = MainPage()
    search = SearchPage()
    results = SearchResultsPage()

    with allure.step("Открыть главную страницу"):
        main.open()

    with allure.step("Открыть поиск из шапки сайта"):
        main.open_search()

    with allure.step("Проверить, что открылась страница поиска"):
        search.should_be_opened()

    with allure.step("Проверить, что поле поиска пустое и плейсхолдер корректный"):
        search.should_have_empty_input_and_placeholder()

    with allure.step("Ввести в поиск запрос «Госуслуги»"):
        search.type_query("Госуслуги")

    with allure.step("Выполнить поиск"):
        search.submit()

    with allure.step("Проверить, что открылась страница результатов поиска"):
        results.should_be_opened()

    with allure.step("Проверить, что список результатов не пустой"):
        results.should_have_results()

    with allure.step("Проверить, что первая карточка содержит текст «Госуслуги»"):
        results.first_result_should_contain("Госуслуги")
