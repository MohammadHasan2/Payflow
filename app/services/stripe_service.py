import stripe
from ..config import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def create_checkout_session(amount, merchant):

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": "Order Payment"
                },
                "unit_amount": amount * 100,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://localhost:8000/success",
        cancel_url="http://localhost:8000/cancel",
    )

    return session