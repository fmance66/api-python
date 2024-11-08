from fastapi import FastAPI
from routers import users, products, basic_auth, jwt_auth, users_db
from fastapi.staticfiles import StaticFiles      # para exponer carpeta static

app = FastAPI()
    
# python -m uvicorn main:app --reload        levanta el servidor

# en http://localhost:8000/docs está la doc de swagger
# en http://localhost:8000/redoc está la doc de redoc

# en http://localhost:8000/static/images/python.png están las imagenes
# en http://localhost:8000/static/images/python.jpg están las imagenes

# Routers
app.include_router(users.router)
app.include_router(products.router)

app.include_router(basic_auth.router)
app.include_router(jwt_auth.router)

app.include_router(users_db.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
 
@app.get("/")
async def read_root():
    return "Fastapi API main"

@app.get("/url")
async def read_root():
    return { "url": "https://main-it.com.ar"}
