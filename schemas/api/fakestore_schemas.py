PRODUCT_REQUEST_SCHEMA = {
    "type": "object",
    "required": ["title", "price", "description", "image", "category"],
    "properties": {
        "title": {"type": "string", "minLength": 1},
        "price": {"type": "number", "exclusiveMinimum": 0},
        "description": {"type": "string", "minLength": 1},
        "image": {"type": "string", "minLength": 1},
        "category": {"type": "string", "minLength": 1},
    },
}

PRODUCT_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "price", "description", "image", "category"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "price": {"type": "number"},
        "description": {"type": "string"},
        "image": {"type": "string"},
        "category": {"type": "string"},
    },
}

PRODUCTS_LIST_SCHEMA = {"type": "array", "items": PRODUCT_RESPONSE_SCHEMA}

CART_REQUEST_SCHEMA = {
    "type": "object",
    "required": ["userId", "date", "products"],
    "properties": {
        "userId": {"type": "integer", "minimum": 1},
        "date": {"type": "string", "minLength": 1},
        "products": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["productId", "quantity"],
                "properties": {
                    "productId": {"type": "integer", "minimum": 1},
                    "quantity": {"type": "integer", "minimum": 1},
                },
            },
        },
    },
}

CART_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["id", "date", "products"],
    "properties": {
        "id": {"type": "integer"},
        "userId": {"type": "integer"},
        "user_id": {"type": "integer"},
        "date": {"type": "string"},
        "products": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["quantity"],
                "properties": {
                    "productId": {"type": "integer"},
                    "product_id": {"type": "integer"},
                    "quantity": {"type": "integer"},
                },
                "anyOf": [
                    {"required": ["productId"]},
                    {"required": ["product_id"]},
                ],
            },
        },
    },
}

CARTS_LIST_SCHEMA = {"type": "array", "items": CART_RESPONSE_SCHEMA}

USER_REQUEST_SCHEMA = {
    "type": "object",
    "required": ["email", "username", "password"],
    "properties": {
        "email": {"type": "string", "minLength": 3},
        "username": {"type": "string", "minLength": 1},
        "password": {"type": "string", "minLength": 1},
    },
}

USER_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["id", "email", "username", "password"],
    "properties": {
        "id": {"type": "integer"},
        "email": {"type": "string"},
        "username": {"type": "string"},
        "password": {"type": "string"},
    },
}

USERS_LIST_SCHEMA = {"type": "array", "items": USER_RESPONSE_SCHEMA}

USER_CREATE_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["id"],
    "properties": {
        "id": {"type": "integer", "minimum": 1},
    },
}
