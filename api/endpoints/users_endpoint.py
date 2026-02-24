from api.endpoints.base_endpoint import BaseEndpoint
from models.api.fakestore_models import CreateUserRequest


class UsersEndpoint(BaseEndpoint):
    def get_users(self):
        return self._request("GET", "/users")

    def get_user(self, user_id: int):
        return self._request("GET", f"/users/{user_id}")

    def create_user(self, payload: CreateUserRequest):
        return self._request("POST", "/users", json=payload.model_dump())

    def delete_user(self, user_id: int):
        return self._request("DELETE", f"/users/{user_id}")
