from pydantic import BaseModel
from typing import List

class PedidoItem(BaseModel):
    producto_id: str
    cantidad: int

class Pedido(BaseModel):
    items: List[PedidoItem]
    total: float