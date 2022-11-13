from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from cart.models import Order


def get_new_order_url():
    return urlsafe_base64_encode(force_bytes(Order.objects.count() + 1))


def make_order(request, order_url):
    return request.user.get_order(request, order_url)
