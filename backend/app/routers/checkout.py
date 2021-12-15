import stripe as Stripe
# price_id = 'price_1K6tdcDCMyBp4fywVCBBhT56' publishable_key =
# pk_test_51K6tTMDCMyBp4fywEgHpdA3cJMH9U9JgLRfjTRRdAcRTFRlmB9ASQU5opWe2w2C7jAvZVacy4fTpWEmEGk67taPJ003WXuRI14
# sk_test_51K6tTMDCMyBp4fyw5zOg8gkUdgBx7OH8T5W8VkHzahkvXjNl8FFzibemAPd7yNdKSA943FnTcrVW398fd2vnQEkb00nPUjK8Ct
from fastapi import APIRouter
from requests import Request

router = APIRouter()

stripe = Stripe.api_key(
    "sk_test_51K6tTMDCMyBp4fyw5zOg8gkUdgBx7OH8T5W8VkHzahkvXjNl8FFzibemAPd7yNdKSA943FnTcrVW398fd2vnQEkb00nPUjK8Ct")


@router.post("/checkout")
async def create_checkout(request: Request):
    data = await request.json()
    print(data)
    checkout = Stripe.Checkout.Session.create(
        customer_email=data['email'],
        payment_method_types=['card'],
        line_items=[{
            "price": data['price_id'],
            "quantity": data['quantity']
        }],
        mode='payment',
        success_url='${request.url_root}/success',
        cancel_url='${request.url_root}/cancel'
    )
    return {'session_id': checkout.id}


@router.get("/success")
async def success():
    return {'success': True}


@router.get("/cancel")
async def cancel():
    return {'success': False}


@router.post("/billing")
async def create_billing_portal(request: Request):
    data = await request.json()
    print(data)
    billing = Stripe.BillingPortal.Session.create(
        customer_email=data['email'],
        payment_method_types=['card'],
        line_items=[{
            "price": data['price_id'],
            "quantity": data['quantity']
        }],
        mode='payment',
        success_url='${request.url_root}/success',
        cancel_url='${request.url_root}/cancel'
    )
    return {'session_id': billing.id}
