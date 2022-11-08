from django.urls import path

from cart.views import CartView, CartItemDelete, CartItemAdd, SubmitOrder, OrderView, OrderListView

urlpatterns = [
    # Views
    path('cart/', CartView.as_view(), name='cart'),
    path('orders/', OrderListView.as_view(), name='order'),
    path('order/<slug:order_url>', OrderView.as_view(), name='order'),

    path('submit-order/', SubmitOrder.as_view(), name='submit-order'),

    # Cart items operations
    path('cart-delete/', CartItemDelete.as_view(), name='del_from_cart'),
    path('cart-add/', CartItemAdd.as_view(), name='add_to_cart'),
]
