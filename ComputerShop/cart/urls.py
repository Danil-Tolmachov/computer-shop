from django.urls import path

from cart.views import CartView, CartItemDelete, CartItemAdd

urlpatterns = [
    # Views
    path('cart/', CartView.as_view(), name='cart'),

    # Cart items operations
    path('cart-delete/', CartItemDelete.as_view(), name='del_from_cart'),
    path('cart-add/', CartItemAdd.as_view(), name='add_to_cart')
]
