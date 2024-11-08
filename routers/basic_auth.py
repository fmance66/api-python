from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix = "/basic",
                   tags=["basic_auth"])

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    id: int
    username: str
    nombre: str
    apellido: str
    email: str
    disabled: bool

class UserDB(User):             # es User + password
    password: str

users_db = {
    "fmancevich": {
        "id": 1,
        "username": "fmancevich",
        "nombre": "Fernando",
        "apellido": "Mancevich",
        "email": "fmancevich@main-it.com",
        "disabled": False,
        "password": "mega08ne"
    },
    "rosmartinez": {
        "id": 2,
        "username": "rosmartinez",
        "nombre": "Rosana Andrea",
        "apellido": "Martínez",
        "email": "rosmartinez69@gamil.com",
        "disabled": False,
        "password": "dafnea05"
    },
    "sojeda": {
        "id": 3,
        "username": "sojeda",
        "nombre": "Hernán",
        "apellido": "Ojeda",
        "email": "sojeda@arca.com.ar",
        "disabled": True,
        "password": "pararayo70"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
# criterio de dependencia
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = f"Token no autorizado, credenciales de autenticación inválidas",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    if user.disabled:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = f"Usuario {user.username} inactivo"
        )
    # del user.password
    return user

# el login se hace con un form OAuth2PasswordRequestForm y obtiene el token
@router.post("/login")             
async def login(form: OAuth2PasswordRequestForm = Depends()):

    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = f"Usuario {form.username} inexistente"
        )
    
    user = search_user_db(form.username)
    if form.password != user.password:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = f"Usuario {form.username} contraseña incorrecta"
        )

    return {
        "access_token": user.username,      # en este ejemplo el token es el username para hacerlo facil
        "token_type": "bearer"
    }    

# devuelve un usuario (sin la password) si está autenticado (token que es el usuario)
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
