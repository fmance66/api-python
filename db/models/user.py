from pydantic import BaseModel, Field
# from typing import Optional              # no me estaría andando

class User(BaseModel):
    # id: str | None                # no me estaría andando
    # id: Optional[str]             # no me estaría andando
    id: str = Field(None)
    username: str
    nombre: str
    apellido: str
    email: str
