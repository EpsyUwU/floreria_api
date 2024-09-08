from pydantic import BaseModel
from typing import List, Optional

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

class PedidoItemUpdate(BaseModel):
    producto_id: str
    cantidad: int

class PedidoUpdate(BaseModel):
    items: Optional[List[PedidoItemUpdate]] = None

class PedidoDelete(BaseModel):
    message: str

