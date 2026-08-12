import stripe
from django.conf import settings

from core.models import Course, Lesson

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(product: 'Course | Lesson') -> stripe.Product:
    """Создаёт продукт в Stripe."""
    if isinstance(product, Course):
        name = f'Курс: {product.title}'
    else:
        name = f'Урок: {product.title}'

    stripe_product = stripe.Product.create(
        name=name,
        description=product.description,
    )
    return stripe_product


def create_stripe_price(product: stripe.Product, price: int) -> stripe.Price:
    """Создаёт цену в Stripe."""
    price = stripe.Price.create(
        currency='rub',
        unit_amount=int(price * 100),
        product=product.id,
    )
    return price


def create_stripe_checkout_session(price_id: str) -> stripe.checkout.Session:
    """Создаёт сессию оплаты и объект Stripe класса Session."""
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url="http://127.0.0.1:8000/success/",
        cancel_url="http://127.0.0.1:8000/cancel/",
    )
    return session
