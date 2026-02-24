import allure
import pytest
from jsonschema import validate

from api.endpoints.carts_endpoint import CartsEndpoint
from models.api.fakestore_models import CartProductItem, CartResponse, CreateCartRequest
from schemas.api.fakestore_schemas import (
    CART_REQUEST_SCHEMA,
    CART_RESPONSE_SCHEMA,
    CARTS_LIST_SCHEMA,
)
from tests.marks import component, jira_issues, layer, microservice, owner, tm4j

pytestmark = [
    layer("api"),
    owner("goncharov"),
    component("carts"),
    microservice("FakeStore API"),
    allure.label("suite", "API"),
    allure.label("subSuite", "Carts"),
    allure.epic("API RuStore Diploma"),
    allure.feature("Carts"),
]


class TestCartsApi:
    @allure.tag("API", "Carts", "Smoke")
    @allure.story("Получение списка корзин")
    @allure.title("Список корзин возвращается со статусом 200")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.id("FAKESTORE-API-007")
    @tm4j("FAKESTORE-API-007")
    @jira_issues("DIP-API-107")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_carts_returns_200_and_schema(self, api_session, api_timeout):
        endpoint = CartsEndpoint(api_session, api_timeout)

        with allure.step("Отправить GET /carts"):
            response = endpoint.get_carts()

        with allure.step("Проверить статус и схему ответа"):
            assert response.status_code == 200
            body = response.json()
            assert len(body) > 0
            validate(instance=body, schema=CARTS_LIST_SCHEMA)

    @allure.tag("API", "Carts")
    @allure.story("Создание корзины")
    @allure.title("Создание корзины через POST /carts возвращает 201")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.id("FAKESTORE-API-008")
    @tm4j("FAKESTORE-API-008")
    @jira_issues("DIP-API-108")
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_cart_returns_201_and_expected_data(self, api_session, api_timeout):
        endpoint = CartsEndpoint(api_session, api_timeout)
        payload = CreateCartRequest(
            userId=1,
            date="2020-02-03",
            products=[CartProductItem(product_id=5, quantity=1)],
        )

        with allure.step("Провалидировать request-схему"):
            validate(instance=payload.model_dump(by_alias=True), schema=CART_REQUEST_SCHEMA)

        with allure.step("Отправить POST /carts"):
            response = endpoint.create_cart(payload)

        with allure.step("Проверить статус, значения и схему ответа"):
            assert response.status_code == 201
            body = response.json()
            parsed = CartResponse(**body)
            if parsed.user_id is not None:
                assert parsed.user_id == payload.user_id
            assert parsed.products[0].product_id == payload.products[0].product_id
            validate(instance=body, schema=CART_RESPONSE_SCHEMA)
