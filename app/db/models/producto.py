from pydantic import BaseModel

class Producto(BaseModel):
    nombre: str
    precio: float
    stock: int