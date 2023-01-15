from django.urls import path

from cart.views import CartItemSet, CartView, CartItemDelete, CartItemAdd, SubmitOrder, OrderView, OrderListView

urlpatterns = [
    #  Views
    path('cart/', CartView.as_view(), name='cart'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('order/<slug:order_url>', OrderView.as_view(), name='order'),

    #  Cart items operations
    path('cart-delete/', CartItemDelete.as_view(), name='del_from_cart'),
    path('cart-add/', CartItemAdd.as_view(), name='add_to_cart'),
    path('cart-set/', CartItemSet.as_view(), name='set_product_count'),

    #  Order release
    path('submit-order/', SubmitOrder.as_view(), name='submit-order'),
]
