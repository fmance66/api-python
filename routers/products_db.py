# Clase en vídeo: https://youtu.be/_y9qQZXE24A?t=20480

### products DB API ###

from fastapi import APIRouter, HTTPException, status
from db.models.product import Product
from db.schemas.product import product_schema, products_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/productdb",
                   tags=["productdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

products_list = []


@router.get("/")
async def product():
    return {
        "estado": "OK",
        "mensaje": "Fastapi API, recurso productdb"
    }


# @router.get("/all", response_model=list[Product])
@router.get("/all")
async def products():
    return {
        "estado": "OK",
        "mensaje": "Lista de productos encontrados",
        "data": products_schema(db_client.products.find())
    }
    

@router.get("/{id}")
async def product(id: str):
    print("id:", str)
    return search_product("_id", ObjectId(id))


# @router.get("/")                    # tiene que tener la '/' para que funcione                       
# async def product(id: str):
#     return search_product(id)


@router.get("/search/q")            # si no agrego search no funciona ???                    
async def product(id: str):
    return search_product("_id", ObjectId(id))


# @router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def product(product: Product):
    print("post -> product:", product)

    if search_product("nombre", product.nombre)["estado"] == "OK":
        raise HTTPException(
            status_code = status.HTTP_406_NOT_ACCEPTABLE, 
            detail = "El producto ya existe"
        )

    product_dict = dict(product)
    del product_dict["id"]

    id = db_client.products.insert_one(product_dict).inserted_id          # inserto el producto

    new_product = product_schema(db_client.products.find_one({"_id": id}))   # busco el producto insertado

    return {
        "estado": "OK",
        "mensaje": "Producto agregado correctamente",
        "data": Product(**new_product)
    }


# @router.put("/", response_model=Product, status_code=status.HTTP_200_OK)
@router.put("/", status_code=status.HTTP_200_OK)
async def product(product: Product):

    product_dict = dict(product)
    # del product_dict["id"]             # lo elimina para que no lo modifique?
    print(product_dict)

    try:
        db_client.products.find_one_and_replace({ "_id": ObjectId(product.id) }, product_dict)
    except:
        return {
            "estado": "ERROR",
            "mensaje": "No se pudo actualizar el producto"
        }

    product_update = search_product("_id", ObjectId(product.id))     # busca el producto actualizado

    if product_update["estado"] == "OK":
        return {
            "estado": "OK",
            "mensaje": "Producto modificado correctamente",
            "data": product_update["data"]
        }
    else:
        return {
            "estado": "ERROR",
            "mensaje": "Producto no encontrado"
        }


@router.delete("/{id}", status_code=status.HTTP_200_OK)
# @router.delete("/{id}")
async def product(id: str):

    found = db_client.products.find_one_and_delete({"_id": ObjectId(id)})
    print("found ->", found)

    if not found:
            raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "No se encontró el producto a eliminar"
        )

    return {
        "estado": "OK",
        "mensaje": "Producto eliminado correctamente",
        "id": id
    }


def search_product(field: str, key):
    print("search_product -> field:", field, "  key:", key)
    try:
        product = db_client.products.find_one({field: key})
        return {
            "estado": "OK",
            "mensaje": "Producto encontrado",
            "data": Product(**product_schema(product))
        }
    # except Exception as error:
    except Exception:
        # print(error)
        return {
            "estado": "ERROR",
            # "mensaje": f"No se encontró el producto con id: {key}, {error}"
            "mensaje": f"No se encontró el producto con id: {key}"
        }
        
