# from fastapi import FastAPI, HTTPException
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# app = FastAPI()
router = APIRouter(prefix = "/product",
                   tags=["product"],
                   responses={ 404: {"message": "No encontrado"} }
         )

## python -m uvicorn products:app --reload        levanta el servidor

# en http://localhost:8000/docs está la doc de swagger
# en http://localhost:8000/redoc está la doc de redoc

class Product(BaseModel):
    id: int
    descripcion: str
    grupo: str
    precio: float

products_list = [
    Product(id = 1, descripcion = "mouse inhalambrico", grupo = "mouses", precio = 12990.90),
    Product(id = 2, descripcion = "disco ssd", grupo = "discos", precio = 98970.00),
    Product(id = 3, descripcion = "teclado con luz", grupo = "teclados", precio = 18350.50 )
]

@router.get("/")
async def product():
    return "Fastapi API, recurso product"

@router.get("/all")
async def product():
    return products_list                 # python list of Product BaseModel

@router.get("/{id}")
async def product(id: int):
    return search_product(id)

@router.get("/")                    # tiene que tener la '/' para que funcione                       
async def product(id: int):
    return search_product(id)

@router.get("/search/q")            # si no agrego search no funciona ???                    
async def product(id: int):
    return search_product(id)

@router.post("/", status_code = 201)                                    
async def product(product: Product):
    resultado = add_product(product)
    print("resultado ->", resultado)
    if resultado["estado"] == "ok":
        return {
            "estado": "ok",
            "mensaje": "Producto agregado correctamente",
            "data": product
        }
    else:
        raise HTTPException(status_code = 404, detail = f"{resultado['error']}")
        # return {
        #     "estado": "error",
        #     "error": f"{resultado['error']}"
        # }

@router.put("/")                                    
async def product(product: Product):
    resultado = update_product(product)
    # print("resultado ->", resultado)
    if resultado["estado"] == "ok":
        return {
            "estado": "ok",
            "mensaje": "Producto modificado correctamente",
            "data": product
        }
    else:
        return {
            "estado": "error",
            "error": f"{resultado['error']}"
        }

@router.delete("/{id}")                                    
async def product(id: int):
    resultado = erase_product(id)
    # print("resultado ->", resultado)
    if resultado["estado"] == "ok":
        return {
            "estado": "ok",
            "mensaje": "Producto eliminado correctamente",
            "id": id
        }
    else:
        return {
            "estado": "error",
            "error": f"{resultado['error']}"
        }

def search_product(id: int):
    # print("search_product -> id:", id)
    try:
        productid = lambda product: product.id == id
        products = list(filter(productid, products_list))      # products porque puede devolver mas de uno
        return {
            "estado": "ok",
            "data": products[0]
        }
    except Exception as error:
        return {
            "estado": "error",
            "error": f"No se encontró el producto con id: {id}, {error}"
        }

def modify_product(product: Product):
    found = False
    try:
        for index, product_saved in enumerate(products_list):
            if product_saved.id == product.id:
                products_list[index] = product    # actualiza el product en la lista
                return {
                    "estado": "ok",
                    "mensaje": "Producto modificado correctamente"
                }
        if not found:
            return {
                "estado": "error",
                "error": f"No se encontró el producto con id: {product.id}"
            }

        
    except Exception as error:
        return {
            "estado": "error",
            "error": f"No se puede modificar el producto con id: {product.id}, {error}"
        }

def add_product(product: Product):
    try:
        print("add_product -> product:", product)
        found = search_product(product.id)
        print("found ->", found)
        if found["estado"] == "ok":
            return { 
                "estado": "error",
                "error": f"producto con id: {product.id} ya se encuentra en la base"
            }
        else :
            products_list.append(product)
            return {
                "estado": "ok",
                "mensaje": "Producto agregado correctamente"
            }

    except Exception as error:
        return {
            "estado": "error",
            "error": f"error al agregar el producto con id: {product.id}, {error}"
        }

def update_product(product: Product):
    print("update_product -> product:", product)
    found = modify_product(product)
    print("found ->", found)

    if found["estado"] == "ok":
        return {
            "estado": "ok",
            "mensaje": "Producto actualizado correctamente"
        }
    else :
        return {
            "estado": "error",
            "error": f"{found['error']}"
        }

def erase_product(id: int):
    found = False
    try:
        for index, product_saved in enumerate(products_list):
            if product_saved.id == id:
                del products_list[index]     # elimina el product de la lista
                return {
                    "estado": "ok",
                    "mensaje": "Producto eliminado correctamente"
                }
        if not found:
            return {
                "estado": "error",
                "error": f"No se encontró el producto con id: {id}"
            }

        
    except Exception as error:
        return {
            "estado": "error",
            "error": f"No se puede eliminar el producto con id: {id}, {error}"
        }
