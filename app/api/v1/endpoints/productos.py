from fastapi import APIRouter, HTTPException, Depends
from app.schemas.producto import ProductoCreate, ProductoResponse, DeleteResponse, ProductoUpdate
from app.db.crud.producto_crud import create_producto, get_productos, get_producto_by_id, delete_producto_by_id, update_producto_by_id
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=ProductoResponse)
def crear_producto(producto: ProductoCreate, db = Depends(get_db)):
    try:
        nuevo_producto = create_producto(producto, db)
        return nuevo_producto
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ProductoResponse])
def listar_productos(db = Depends(get_db)):
    productos = get_productos(db)
    return productos

@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: str, db = Depends(get_db)):
    try:
        producto = get_producto_by_id(db, producto_id)
        if producto is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return producto
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{producto_id}", response_model=DeleteResponse)
def eliminar_producto(producto_id: str, db = Depends(get_db)):
    try:
        producto = delete_producto_by_id(db, producto_id)
        if producto is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return producto
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: str, producto: ProductoUpdate, db = Depends(get_db)):
    try:
        producto = update_producto_by_id(db, producto_id, producto)
        if producto is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return producto
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))