from fastapi import FastAPI
from app.api.v1.endpoints import productos, pedidos

app = FastAPI()

# Incluir los routers para productos y pedidos
app.include_router(productos.router, prefix="/api/v1/productos", tags=["productos"])
app.include_router(pedidos.router, prefix="/api/v1/pedidos", tags=["pedidos"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
