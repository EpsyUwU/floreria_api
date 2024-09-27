from fastapi import APIRouter, HTTPException, Depends
from app.schemas.mercadopago import PaymentResponse, PaymentRequest
import mercadopago
from dotenv import load_dotenv
import os

router = APIRouter()

load_dotenv()
token = os.getenv("ACCESS_TOKEN_MERCADOPAGO")

sdk = mercadopago.SDK(token)

@router.post('/mercadopago/', response_model=PaymentResponse)
def crear_preferencia(payment_request: PaymentRequest):
    try:
        preference_data = {
            "items": [
                {
                    "title": payment_request.title,
                    "quantity": payment_request.quantity,
                    "currency_id": "MXN",
                    "unit_price": payment_request.price
                }
            ],
            "back_urls": {
                "success": "https://youtu.be/xvFZjo5PgG0?si=sKj8k1NQTptHh5OZ",
                "failure": "https://www.tuweb.com/failure",
                "pending": "https://www.tuweb.com/pending"
            },
            "auto_return": "approved"
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        return PaymentResponse(id=preference["id"], init_point=preference["init_point"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear preferencia: {str(e)}")