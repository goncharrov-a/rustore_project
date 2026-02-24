from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class CreateProductRequest(BaseModel):
    title: str = Field(min_length=1)
    price: float = Field(gt=0)
    description: str = Field(min_length=1)
    image: str = Field(min_length=1)
    category: str = Field(min_length=1)


class ProductResponse(CreateProductRequest):
    id: int


class CartProductItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    product_id: int = Field(
        ge=1,
        validation_alias=AliasChoices("productId", "product_id"),
        serialization_alias="productId",
    )
    quantity: int = Field(ge=1)


class CreateCartRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: int = Field(ge=1, alias="userId")
    date: str = Field(min_length=1)
    products: list[CartProductItem]


class CartResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    user_id: int | None = Field(
        default=None,
        validation_alias=AliasChoices("userId", "user_id"),
        serialization_alias="userId",
    )
    date: str
    products: list[CartProductItem]


class CreateUserRequest(BaseModel):
    email: str = Field(min_length=3)
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class UserResponse(CreateUserRequest):
    id: int


class CreatedEntityResponse(BaseModel):
    id: int = Field(ge=1)
