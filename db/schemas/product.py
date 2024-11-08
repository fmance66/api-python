def product_schema(product) -> dict:
    return {
        "id": str(product["_id"]),
        "nombre": product["nombre"],
        "descripcion": product["descripcion"],
        "categoria": product["categoria"],
        "precio": product["precio"]
    }


def products_schema(products) -> list:
    return [product_schema(product) for product in products]