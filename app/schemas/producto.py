from pydantic import BaseModel

class ProductoCreate(BaseModel):
    nombre: str
    precio: float
    stock: int

class ProductoResponse(ProductoCreate):
    id: str

class DeleteResponse(BaseModel):
    message: str

class ProductoUpdate(BaseModel):
    nombre: str
    precio: float
    stock: int
