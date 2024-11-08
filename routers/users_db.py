# Clase en vídeo: https://youtu.be/_y9qQZXE24A?t=20480

### Users DB API ###

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

users_list = []


@router.get("/")
async def user():
    return {
        "estado": "OK",
        "mensaje": "Fastapi API, recurso userdb"
    }


# @router.get("/all", response_model=list[User])
@router.get("/all")
async def users():
    return {
        "estado": "OK",
        "mensaje": "Lista de usuarios encontrados",
        "data": users_schema(db_client.users.find())
    }
    

@router.get("/{id}")
async def user(id: str):
    print("id:", str)
    return search_user("_id", ObjectId(id))


# @router.get("/")                    # tiene que tener la '/' para que funcione                       
# async def user(id: int):
#     return search_user(id)


@router.get("/search/q")            # si no agrego search no funciona ???                    
async def user(id: int):
    return search_user(id)


# @router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def user(user: User):
    print("post -> user:", user)

    if search_user("username", user.username)["estado"] == "OK":
        raise HTTPException(
            status_code = status.HTTP_406_NOT_ACCEPTABLE, 
            detail = "El usuario ya existe"
        )

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id          # inserto el usuario

    new_user = user_schema(db_client.users.find_one({"_id": id}))   # busco el usuario insertado

    return {
        "estado": "OK",
        "mensaje": "Usuario agregado correctamente",
        "data": User(**new_user)
    }


# @router.put("/", response_model=User, status_code=status.HTTP_200_OK)
@router.put("/", status_code=status.HTTP_200_OK)
async def user(user: User):

    user_dict = dict(user)
    # del user_dict["id"]             # lo elimina para que no lo modifique?

    try:
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
    except:
        return {
            "estado": "ERROR",
            "mensaje": "No se pudo actualizar el usuario"
        }

    user_update = search_user("_id", ObjectId(user.id))     # busca el usuario actualizado

    return {
        "estado": "OK",
        "mensaje": "Usuario modificado correctamente",
        "data": user_update["data"]
    }


@router.delete("/{id}", status_code=status.HTTP_200_OK)
# @router.delete("/{id}")
async def user(id: str):

    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    print("found ->", found)

    if not found:
            raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "No se encontró el usuario a eliminar"
        )

    return {
        "estado": "OK",
        "mensaje": "Usuario eliminado correctamente",
        "id": id
    }


def search_user(field: str, key):
    print("search_user -> id:", id)
    try:
        user = db_client.users.find_one({field: key})
        return {
            "estado": "OK",
            "mensaje": "Usuario encontrado",
            "data": User(**user_schema(user))
        }
    except Exception as error:
        return {
            "estado": "ERROR",
            "mensaje": f"No se encontró el usuario con id: {id}, {error}"
        }
