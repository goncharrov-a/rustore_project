from api.endpoints.base_endpoint import BaseEndpoint
from models.api.fakestore_models import CreateCartRequest


class CartsEndpoint(BaseEndpoint):
    def get_carts(self):
        return self._request("GET", "/carts")

    def create_cart(self, payload: CreateCartRequest):
        return self._request("POST", "/carts", json=payload.model_dump(by_alias=True))
