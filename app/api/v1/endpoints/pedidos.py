from fastapi import APIRouter, HTTPException, Depends
from app.schemas.pedido import PedidoCreate, PedidoResponse
from app.db.crud.pedido_crud import create_pedido, get_pedidos, get_pedido_by_id
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=PedidoResponse)
def crear_pedido(pedido: PedidoCreate, db = Depends(get_db)):
    try:
        nuevo_pedido = create_pedido(pedido, db)
        return nuevo_pedido
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[PedidoResponse])
def listar_pedidos(db = Depends(get_db)):
    pedidos = get_pedidos(db)
    return pedidos

@router.get("/{pedido_id}", response_model=PedidoResponse)
def obtener_pedido(pedido_id: str, db = Depends(get_db)):
    pedido = get_pedido_by_id(db, pedido_id)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido
