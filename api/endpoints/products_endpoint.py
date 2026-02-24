from api.endpoints.base_endpoint import BaseEndpoint
from models.api.fakestore_models import CreateProductRequest


class ProductsEndpoint(BaseEndpoint):
    def get_products(self):
        return self._request("GET", "/products")

    def get_product(self, product_id: int):
        return self._request("GET", f"/products/{product_id}")

    def create_product(self, payload: CreateProductRequest):
        return self._request("POST", "/products", json=payload.model_dump())

    def delete_product(self, product_id: int):
        return self._request("DELETE", f"/products/{product_id}")
