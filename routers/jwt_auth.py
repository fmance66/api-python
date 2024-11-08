from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

# algoritmo de encriptación
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1              # un minuto
# generado con 'openssl rand -hex 32'
SECRET = "b1af7a0b27f753e146f2689e503fbfa05640206b6873f3145a14eb17a3045c07"     

router = APIRouter(prefix = "/jwt",
                   tags=["jwt_auth"])

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# contexto de encriptación
crypt = CryptContext(schemes=["bcrypt"])

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
        "password": "$2a$12$aOE9eZ8/1rg1A1EtjjY/8uA8utPztJnc7Z0UOXzIUk95fSoMT1.OK"     # "mega08ne"
    },
    "rosmartinez": {
        "id": 2,
        "username": "rosmartinez",
        "nombre": "Rosana Andrea",
        "apellido": "Martínez",
        "email": "rosmartinez69@gamil.com",
        "disabled": False,
        "password": "$2a$12$DJFW6Ul1hl/nq6kV4XKPNON3bgTTWLJVFFRC2cnGRz9DI2kLoYQUy"     # "dafnea05"
    },
    "sojeda": {
        "id": 3,
        "username": "sojeda",
        "nombre": "Hernán",
        "apellido": "Ojeda",
        "email": "sojeda@arca.com.ar",
        "disabled": True,
        "password": "$2a$12$uU5.ZNPx1cx7h50CieJBW.EpKNajtszdAjrpo9IYcqqfvesj9o3hq"    # "pararayo70"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token: str = Depends(oauth2)):

    def exception(error): 
        return HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = f"JWT error: {error}",
            headers = {"WWW-Authenticate": "Bearer"}
        )

    try:
        # username es el sub guardado en el jwt
        username = jwt.decode(token, SECRET, algorithms = [ALGORITHM]).get("sub")   
        if username is None:
            raise exception("No se pudo decodificar el usuario")
        
    except JWTError as error:
        raise exception(error)
    
    return search_user(username)            # devuelve el usuario
    
# criterio de dependencia
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = f"Usuario {user.username} inactivo"
        )
    return user

# el login se hace con un form OAuth2PasswordRequestForm, maneja claves encriptadas
@router.post("/login")             
async def login(form: OAuth2PasswordRequestForm = Depends()):

    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = f"Usuario {form.username} inexistente"
        )
    
    user = search_user_db(form.username)

    # verifica la clave contra la clave encriptada en la base
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = f"Usuario {form.username} contraseña incorrecta"
        )

    # calcula la hora de expiración como la hora actual mas un minuto (ACCESS_TOKEN_DURATION)
    expire_time = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_DURATION)

    access_token = {
        "sub": user.username,
        "exp": expire_time
    }

    # crea un token seguro
    return {
        "access_token": jwt.encode(access_token, SECRET, algorithm = ALGORITHM),      # token seguro
        "token_type": "jwt"
    }    

# devuelve un usuario (sin la password) si está autenticado (token jwt)
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
