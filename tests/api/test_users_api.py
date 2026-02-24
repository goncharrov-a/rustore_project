import allure
import pytest
from jsonschema import validate

from api.endpoints.users_endpoint import UsersEndpoint
from models.api.fakestore_models import CreatedEntityResponse, CreateUserRequest
from schemas.api.fakestore_schemas import (
    USER_CREATE_RESPONSE_SCHEMA,
    USER_REQUEST_SCHEMA,
    USERS_LIST_SCHEMA,
)
from tests.marks import component, jira_issues, layer, microservice, owner, tm4j

pytestmark = [
    layer("api"),
    owner("goncharov"),
    component("users"),
    microservice("FakeStore API"),
    allure.label("suite", "API"),
    allure.label("subSuite", "Users"),
    allure.epic("API RuStore Diploma"),
    allure.feature("Users"),
]


class TestUsersApi:
    @allure.tag("API", "Users", "Smoke")
    @allure.story("Получение списка пользователей")
    @allure.title("Список пользователей возвращается со статусом 200")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.id("FAKESTORE-API-005")
    @tm4j("FAKESTORE-API-005")
    @jira_issues("DIP-API-105")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_users_returns_200_and_schema(self, api_session, api_timeout):
        endpoint = UsersEndpoint(api_session, api_timeout)

        with allure.step("Отправить GET /users"):
            response = endpoint.get_users()

        with allure.step("Проверить статус и схему ответа"):
            assert response.status_code == 200
            body = response.json()
            assert len(body) > 0
            validate(instance=body, schema=USERS_LIST_SCHEMA)

    @allure.tag("API", "Users")
    @allure.story("Создание пользователя")
    @allure.title("Создание пользователя через POST /users возвращает 201")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.id("FAKESTORE-API-006")
    @tm4j("FAKESTORE-API-006")
    @jira_issues("DIP-API-106")
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_user_returns_201_and_expected_data(self, api_session, api_timeout):
        endpoint = UsersEndpoint(api_session, api_timeout)
        payload = CreateUserRequest(
            email="qa_user@mail.com",
            username="qa_user",
            password="123456",
        )

        with allure.step("Провалидировать request-схему"):
            validate(instance=payload.model_dump(), schema=USER_REQUEST_SCHEMA)

        with allure.step("Отправить POST /users"):
            response = endpoint.create_user(payload)

        with allure.step("Проверить статус, значения и схему ответа"):
            assert response.status_code == 201
            body = response.json()
            parsed = CreatedEntityResponse(**body)
            assert parsed.id >= 1
            validate(instance=body, schema=USER_CREATE_RESPONSE_SCHEMA)
