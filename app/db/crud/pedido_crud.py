from bson import ObjectId
from app.schemas.pedido import PedidoCreate, PedidoResponse, ProductoItemResponse, PedidoUpdate


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

        productos_collection.update_one(
            {"_id": ObjectId(item.producto_id)},
            {"$inc": {"stock": -item.cantidad}}
        )

        item_total = producto["precio"] * item.cantidad
        total += item_total

        producto_responses.append(ProductoItemResponse(
            producto_id=item.producto_id,
            nombre=producto["nombre"],
            cantidad=item.cantidad,
            precio_unitario=producto["precio"],
            total=item_total
        ))


    pedido_dict = pedido.dict()
    pedido_dict["total"] = total
    result = pedidos_collection.insert_one(pedido_dict)

    pedido_insertado = pedidos_collection.find_one({"_id": result.inserted_id})

    return PedidoResponse(
        id=str(pedido_insertado["_id"]),
        items=producto_responses,
        total=pedido_insertado["total"]
    )


def get_pedidos(db):
    cursor = db["pedidos"].find()
    pedidos = list(cursor)

    all_pedidos = []

    for pedido in pedidos:
        producto_responses = []

        for item in pedido["items"]:
            producto = db["productos"].find_one({"_id": ObjectId(item["producto_id"])})
            if producto is None:
                raise ValueError(f"Producto con ID {item['producto_id']} no encontrado")

            item_total = producto["precio"] * item["cantidad"]

            producto_responses.append(ProductoItemResponse(
                producto_id=item["producto_id"],
                nombre=producto["nombre"],
                cantidad=item["cantidad"],
                precio_unitario=producto["precio"],
                total=item_total
            ))

        all_pedidos.append(PedidoResponse(
            id=str(pedido["_id"]),
            items=producto_responses,
            total=pedido["total"]
        ))

    return all_pedidos


def get_pedido_by_id(pedido_id: str, db):
    pedido_id = ObjectId(pedido_id.strip())

    pedido = db["pedidos"].find_one({"_id": pedido_id})
    if pedido is None:
        return None

    producto_responses = []

    for item in pedido.get("items", []):
        producto = db["productos"].find_one({"_id": ObjectId(item["producto_id"])})
        if producto is None:
            continue

        item_total = producto["precio"] * item["cantidad"]

        producto_responses.append(ProductoItemResponse(
            producto_id=item["producto_id"],
            nombre=producto["nombre"],
            cantidad=item["cantidad"],
            precio_unitario=producto["precio"],
            total=item_total
        ))

    return PedidoResponse(
        id=str(pedido["_id"]),
        items=producto_responses,
        total=pedido["total"]
    )

def update_pedido_by_id(pedido_id: str, pedido_update: PedidoUpdate, db):
    pedido_id = ObjectId(pedido_id.strip())

    pedido_existente = db["pedidos"].find_one({"_id": pedido_id})
    if pedido_existente is None:
        return None

    if pedido_update.items is not None:
        productos_collection = db["productos"]
        producto_responses = []
        total = 0

        for item in pedido_update.items:
            producto = productos_collection.find_one({"_id": ObjectId(item.producto_id)})
            if producto is None:
                raise ValueError(f"Producto con ID {item.producto_id} no encontrado")

            if producto["stock"] < item.cantidad:
                raise ValueError(f"No hay suficiente stock para el producto con ID {item.producto_id}")

            productos_collection.update_one(
                {"_id": ObjectId(item.producto_id)},
                {"$inc": {"stock": -item.cantidad}}
            )

            item_total = producto["precio"] * item.cantidad
            total += item_total

            producto_responses.append(ProductoItemResponse(
                producto_id=item.producto_id,
                nombre=producto["nombre"],
                cantidad=item.cantidad,
                precio_unitario=producto["precio"],
                total=item_total
            ))


        items_dict = [item.dict() for item in pedido_update.items]

        update_data = {
            "items": items_dict,
            "total": total
        }
        db["pedidos"].update_one({"_id": pedido_id}, {"$set": update_data})


        pedido_actualizado = db["pedidos"].find_one({"_id": pedido_id})

        return PedidoResponse(
            id=str(pedido_actualizado["_id"]),
            items=producto_responses,
            total=pedido_actualizado["total"]
        )
    else:
        return None


def delete_pedido_by_id(pedido_id: str, db):
    pedido_id = ObjectId(pedido_id.strip())
    pedido = db["pedidos"].find_one({"_id": pedido_id})

    if pedido is None:
        return None

    db["pedidos"].delete_one({"_id": pedido_id})
    return {"message": f"Pedido eliminado"}