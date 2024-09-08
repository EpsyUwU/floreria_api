from pydantic import BaseModel
from typing import List
from app.schemas.producto import ProductoCreate


class PedidoItemCreate(BaseModel):
    producto_id: str
    cantidad: int

class ProductoItemResponse(BaseModel):
    producto_id: str
    nombre: str
    cantidad: int
    precio_unitario: float
    total: float

class PedidoCreate(BaseModel):
    items: List[PedidoItemCreate]

class PedidoResponse(PedidoCreate):
    id: str
    items: List[ProductoItemResponse]
    total: float
