from pydantic import BaseModel

class PaymentRequest(BaseModel):
    title: str
    quantity: int
    price: float

class PaymentResponse(BaseModel):
    id: str
    init_point: str
