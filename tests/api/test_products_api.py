import allure
import pytest
from jsonschema import validate

from api.endpoints.products_endpoint import ProductsEndpoint
from models.api.fakestore_models import CreateProductRequest, ProductResponse
from schemas.api.fakestore_schemas import (
    PRODUCT_REQUEST_SCHEMA,
    PRODUCT_RESPONSE_SCHEMA,
    PRODUCTS_LIST_SCHEMA,
)
from tests.marks import component, jira_issues, layer, microservice, owner, tm4j

pytestmark = [
    layer("api"),
    owner("goncharov"),
    component("products"),
    microservice("FakeStore API"),
    allure.label("suite", "API"),
    allure.label("subSuite", "Products"),
    allure.epic("API RuStore Diploma"),
    allure.feature("Products"),
]


class TestProductsApi:
    @allure.tag("API", "Products", "Smoke")
    @allure.story("Получение списка продуктов")
    @allure.title("Список продуктов возвращается со статусом 200 и валидной схемой")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.id("FAKESTORE-API-001")
    @tm4j("FAKESTORE-API-001")
    @jira_issues("DIP-API-101")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_products_returns_200_and_valid_schema(self, api_session, api_timeout):
        endpoint = ProductsEndpoint(api_session, api_timeout)

        with allure.step("Отправить GET /products"):
            response = endpoint.get_products()

        with allure.step("Проверить статус и схему ответа"):
            assert response.status_code == 200
            body = response.json()
            assert len(body) > 0
            validate(instance=body, schema=PRODUCTS_LIST_SCHEMA)

    @allure.tag("API", "Products")
    @allure.story("Получение продукта по id")
    @allure.title("Продукт по id=1 возвращается со статусом 200")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.id("FAKESTORE-API-002")
    @tm4j("FAKESTORE-API-002")
    @jira_issues("DIP-API-102")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_single_product_returns_expected_fields(self, api_session, api_timeout):
        endpoint = ProductsEndpoint(api_session, api_timeout)

        with allure.step("Отправить GET /products/1"):
            response = endpoint.get_product(1)

        with allure.step("Проверить статус, данные и схему"):
            assert response.status_code == 200
            parsed = ProductResponse(**response.json())
            assert parsed.id == 1
            validate(instance=response.json(), schema=PRODUCT_RESPONSE_SCHEMA)

    @allure.tag("API", "Products")
    @allure.story("Создание продукта")
    @allure.title("Создание продукта через POST /products возвращает 201")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.id("FAKESTORE-API-003")
    @tm4j("FAKESTORE-API-003")
    @jira_issues("DIP-API-103")
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_product_returns_201_and_expected_data(self, api_session, api_timeout):
        endpoint = ProductsEndpoint(api_session, api_timeout)
        payload = CreateProductRequest(
            title="QA diploma product",
            price=10.5,
            description="product for API tests",
            image="https://i.pravatar.cc",
            category="electronics",
        )

        with allure.step("Провалидировать request-схему"):
            validate(instance=payload.model_dump(), schema=PRODUCT_REQUEST_SCHEMA)

        with allure.step("Отправить POST /products"):
            response = endpoint.create_product(payload)

        with allure.step("Проверить статус, значения в response и схему"):
            assert response.status_code == 201
            body = response.json()
            assert body["title"] == payload.title
            assert float(body["price"]) == payload.price
            validate(instance=body, schema=PRODUCT_RESPONSE_SCHEMA)

    @allure.tag("API", "Products")
    @allure.story("Удаление продукта")
    @allure.title("Удаление продукта через DELETE /products/{id}")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.id("FAKESTORE-API-004")
    @tm4j("FAKESTORE-API-004")
    @jira_issues("DIP-API-104")
    @pytest.mark.api
    @pytest.mark.regression
    def test_delete_product_returns_200(self, api_session, api_timeout):
        endpoint = ProductsEndpoint(api_session, api_timeout)

        with allure.step("Отправить DELETE /products/1"):
            response = endpoint.delete_product(1)

        with allure.step("Проверить статус и схему ответа"):
            assert response.status_code == 200
            validate(instance=response.json(), schema=PRODUCT_RESPONSE_SCHEMA)
