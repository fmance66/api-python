# from fastapi import FastAPI, HTTPException
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# app = FastAPI()
router = APIRouter(prefix = "/user",
                   tags=["user"],
                   responses={ 404: {"message": "No encontrado"} }
         )

## python -m uvicorn users:app --reload        levanta el servidor

# en http://localhost:8000/docs está la doc de swagger
# en http://localhost:8000/redoc está la doc de redoc

class User(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str

data_users = [
    {"id": 1, "nombre": "Fernando", "apellido": "Mancevich", "email": "fmancevich@main-it.com.ar"},
    {"id": 2, "nombre": "Carlos", "apellido": "Sainz", "email": "csainz@maferrari.com.it"},
    {"id": 3, "nombre": "Camilo", "apellido": "Capotto", "email": "ccapotto@yahoo.com.ar"}
]

users_list = [
    User(id = 1, nombre =  "Fernando", apellido=  "Mancevich", email=  "fmance66@gmail.com"),
    User(id = 2, nombre =  "Carlos", apellido=  "Sainz", email=  "csainz@maferrari.com.it"),
    User(id = 3, nombre =  "Camilo", apellido=  "Capotto", email=  "ccapotto@yahoo.com.ar")
]

@router.get("/")
async def user():
    return "Fastapi API, recurso user"

@router.get("/all/json")
async def user():
    return data_users                 # json data

@router.get("/all")
async def user():
    print(users_list)
    return users_list                 # python list of User BaseModel

@router.get("/{id}")
async def user(id: int):
    return search_user(id)

@router.get("/")                    # tiene que tener la '/' para que funcione                       
async def user(id: int):
    return search_user(id)

@router.get("/search/q")            # si no agrego search no funciona ???                    
async def user(id: int):
    return search_user(id)

@router.post("/", status_code = 201)                                    
async def user(user: User):
    resultado = add_user(user)
    print("resultado ->", resultado)
    if resultado["estado"] == "ok":
        return {
            "estado": "ok",
            "mensaje": "Usuario agregado correctamente",
            "data": user
        }
    else:
        raise HTTPException(status_code = 404, detail = f"{resultado["error"]}")
        # return {
        #     "estado": "error",
        #     "error": f"{resultado["error"]}"
        # }

@router.put("/")                                    
async def user(user: User):
    resultado = update_user(user)
    # print("resultado ->", resultado)
    if resultado["estado"] == "ok":
        return {
            "estado": "ok",
            "mensaje": "Usuario modificado correctamente",
            "data": user
        }
    else:
        return {
            "estado": "error",
            "error": f"{resultado["error"]}"
        }

@router.delete("/{id}")                                    
async def user(id: int):
    resultado = erase_user(id)
    # print("resultado ->", resultado)
    if resultado["estado"] == "ok":
        return {
            "estado": "ok",
            "mensaje": "Usuario eliminado correctamente",
            "id": id
        }
    else:
        return {
            "estado": "error",
            "error": f"{resultado["error"]}"
        }

def search_user(id: int):
    print("search_user -> id:", id)
    try:
        userid = lambda user: user.id == id
        users = list(filter(userid, users_list))      # users porque puede devolver mas de uno
        return {
            "estado": "ok",
            "data": users[0]
        }
    except Exception as error:
        return {
            "estado": "error",
            "error": f"No se encontró el usuario con id: {id}, {error}"
        }

def modify_user(user: User):
    found = False
    try:
        for index, user_saved in enumerate(users_list):
            if user_saved.id == user.id:
                users_list[index] = user    # actualiza el user en la lista
                return {
                    "estado": "ok",
                    "mensaje": "Usuario modificado correctamente"
                }
        if not found:
            return {
                "estado": "error",
                "error": f"No se encontró el usuario con id: {user.id}"
            }

        
    except Exception as error:
        return {
            "estado": "error",
            "error": f"No se puede modificar el usuario con id: {user.id}, {error}"
        }
    

def add_user(user: User):
    try:
        print("add_user -> user:", user)
        found = search_user(user.id)
        print("found ->", found)
        if found["estado"] == "ok":
            return { 
                "estado": "error",
                "error": f"usuario con id: {user.id} ya se encuentra en la base"
            }
        else :
            users_list.append(user)
            return {
                "estado": "ok",
                "mensaje": "Usuario agregado correctamente"
            }

    except Exception as error:
        return {
            "estado": "error",
            "error": f"error al agregar el usuario con id: {user.id}, {error}"
        }

def update_user(user: User):
    print("update_user -> user:", user)
    found = modify_user(user)
    print("found ->", found)

    if found["estado"] == "ok":
        return {
            "estado": "ok",
            "mensaje": "Usuario actualizado correctamente"
        }
    else :
        return {
            "estado": "error",
            "error": f"{found["error"]}"
        }

def erase_user(id: int):
    found = False
    try:
        for index, user_saved in enumerate(users_list):
            if user_saved.id == id:
                del users_list[index]     # elimina el user de la lista
                return {
                    "estado": "ok",
                    "mensaje": "Usuario eliminado correctamente"
                }
        if not found:
            return {
                "estado": "error",
                "error": f"No se encontró el usuario con id: {id}"
            }

        
    except Exception as error:
        return {
            "estado": "error",
            "error": f"No se puede eliminar el usuario con id: {id}, {error}"
        }
