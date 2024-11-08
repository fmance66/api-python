from pydantic import BaseModel, Field
from enum import Enum

class Categoria(str, Enum):
    discos = 'discos'
    mouses = 'mouses'
    teclados = 'teclados'

class Product(BaseModel):
    id: str = Field(None)
    nombre: str
    descripcion: str
    categoria: Categoria
    precio: float
