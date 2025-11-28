import os
import mercadopago

_payment_provider = None

def get_payment_provider():
    global _payment_provider
    if _payment_provider is None:
        access_token = os.getenv("MERCADO_PAGO_TOKEN")
        if not access_token:
            raise Exception("MERCADO_PAGO_TOKEN is not set")
        _payment_provider = mercadopago.SDK(access_token=access_token)
    return _payment_provider

def generate_pix(value, email):
    payprov = get_payment_provider()
    payment = {
        "transaction_amount": value,
        "description": "Anima AI",
        "payment_method_id": "pix",
        "payer": {
            "email": email
        }
    }

    response = payprov.payment().create(payment)
    payment_info = response["response"]

    if "point_of_interaction" in payment_info:
        pix_qr_code = payment_info["point_of_interaction"]["transaction_data"]["qr_code"]
        payment_id = payment_info["id"]
        return (True, pix_qr_code, payment_id)
    else:
        return (False, None, None)

def check_payment(pgid):
    payprov = get_payment_provider()
    response = payprov.payment().get(pgid)
    payment_info = response["response"]

    if payment_info:
        status = payment_info["status"]
        return status
    else:
        return None
