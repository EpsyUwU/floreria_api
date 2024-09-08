from app.schemas.producto import ProductoCreate, ProductoResponse, ProductoUpdate
from bson import ObjectId

def create_producto(producto: ProductoCreate, db):
    nuevo_producto = producto.dict()
    productos_collection = db["productos"]
    result = productos_collection.insert_one(nuevo_producto)
    producto_insertado = productos_collection.find_one({"_id": result.inserted_id})

    return ProductoResponse(
        id=str(producto_insertado["_id"]),
        nombre=producto_insertado["nombre"],
        precio=producto_insertado["precio"],
        stock=producto_insertado["stock"]
    )

def get_productos(db):
    cursor = db["productos"].find()
    productos = list(cursor)
    return [
        ProductoResponse(
            id=str(producto["_id"]),
            nombre=producto["nombre"],
            precio=producto["precio"],
            stock=producto["stock"]
        )
        for producto in productos
    ]

def get_producto_by_id(db, producto_id: str):
    producto_id = ObjectId(producto_id.strip())
    producto = db["productos"].find_one({"_id": producto_id})
    if producto is None:
        return None
    return ProductoResponse(
        id=str(producto["_id"]),
        nombre=producto["nombre"],
        precio=producto["precio"],
        stock=producto["stock"]
    )

def delete_producto_by_id(db, producto_id: str):
    producto_id = ObjectId(producto_id.strip())
    producto = db["productos"].delete_one({"_id": producto_id})
    if producto is None:
        return None
    return {"message": "Producto eliminado"}

def update_producto_by_id(db, producto_id: str, producto: ProductoUpdate):
    producto_id = ObjectId(producto_id.strip())
    producto_existente = db["productos"].find_one({"_id": producto_id})
    if producto_existente is None:
        return None
    producto_dict = producto.dict()

    result = db["productos"].update_one(
        {"_id": producto_id},
        {"$set": producto_dict}
    )

    if result.matched_count == 0:
        return None

    producto_actualizado = db["productos"].find_one({"_id": producto_id})

    return ProductoResponse(
        id=str(producto_actualizado["_id"]),
        nombre=producto_actualizado["nombre"],
        precio=producto_actualizado["precio"],
        stock=producto_actualizado["stock"]
    )

