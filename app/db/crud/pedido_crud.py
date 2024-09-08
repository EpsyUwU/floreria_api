from bson import ObjectId
from app.schemas.pedido import PedidoCreate, PedidoResponse, ProductoItemResponse


def create_pedido(pedido: PedidoCreate, db):
    total = 0
    items = pedido.items

    productos_collection = db["productos"]
    pedidos_collection = db["pedidos"]

    producto_responses = []

    for item in items:
        producto = productos_collection.find_one({"_id": ObjectId(item.producto_id)})
        if producto is None:
            raise ValueError(f"Producto con ID {item.producto_id} no encontrado")

        if producto["stock"] < item.cantidad:
            raise ValueError(f"No hay suficiente stock para el producto con ID {item.producto_id}")

        # Reducir el stock del producto
        productos_collection.update_one(
            {"_id": ObjectId(item.producto_id)},
            {"$inc": {"stock": -item.cantidad}}
        )

        # Calcular el total basado en el precio y cantidad
        item_total = producto["precio"] * item.cantidad
        total += item_total

        # Agregar detalles del producto a la respuesta
        producto_responses.append(ProductoItemResponse(
            producto_id=item.producto_id,
            nombre=producto["nombre"],
            cantidad=item.cantidad,
            precio_unitario=producto["precio"],
            total=item_total
        ))

    # Crear el nuevo pedido con el total calculado
    pedido_dict = pedido.dict()
    pedido_dict["total"] = total
    result = pedidos_collection.insert_one(pedido_dict)

    # Devolver el pedido con el ID, total calculado, y detalles de los productos
    pedido_insertado = pedidos_collection.find_one({"_id": result.inserted_id})

    return PedidoResponse(
        id=str(pedido_insertado["_id"]),
        items=producto_responses,
        total=pedido_insertado["total"]
    )

def get_pedidos(db):
    return db["pedidos"].find().to_list(None)

def get_pedido_by_id(pedido_id: str, db):
    return db["pedidos"].find_one({"_id": pedido_id})
