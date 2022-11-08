from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView

from cart.models import Product, Cart, ProductItem, Order
from cart.utils import make_order, get_new_order_url
from core.utils import ContextMixin


class CartView(LoginRequiredMixin, ContextMixin, DetailView):
    model = Cart
    template_name = "main/cart.html"
    context_object_name = 'cart'
    extra_context = {'title': 'Cart'}

    # Get current user cart object method
    def get_object(self, queryset=None):
        return self.request.user.cart.pk


class OrderListView(ContextMixin, ListView):
    model = Order
    template_name = "main/orders.html"
    context_object_name = 'orders'
    extra_context = {'title': 'Orders'}

    def get_queryset(self):
        return self.request.user.orders.all()


class OrderView(ContextMixin, DetailView):
    model = Order
    template_name = "main/order.html"
    context_object_name = 'order'
    extra_context = {'title': 'Order tracker'}

    def get_object(self, queryset=None):
        return self.model.objects.get(url=self.kwargs['order_url'])


class CartItemAdd(View):

    @csrf_exempt
    def post(self, request):
        self.item_id = int(request.POST['id'])
        self.product_obj = Product.objects.get(pk=self.item_id)

        self.user_cart = request.user.cart

        # if selected product not in user cart products
        if self.product_obj not in map(lambda x: x.product, self.user_cart.products.all()):
            self.item = ProductItem.objects.create(product=self.product_obj, product_count=1)

            request.user.cart.products.add(self.item)

            # item container context
            data = {
                'pk': self.product_obj.pk,
                'name': self.product_obj.name,
            }

            return JsonResponse(data=data, status=200)
        # else add 1 to product count
        else:
            self.user_product = self.user_cart.products.filter(product=self.product_obj)
            self.user_product.update(product_count=self.user_product.first().product_count+1)

            data = {

            }
            return JsonResponse(data=data, status=304)


class CartItemDelete(View):

    @csrf_exempt
    def post(self, request):
        self.item_id = int(request.POST['id'])
        self.user_cart = request.user.cart

        if Product.objects.get(pk=self.item_id) in map(lambda x: x.product, self.user_cart.products.all()):
            self.product_obj = Product.objects.get(pk=self.item_id)

        else:
            data = {
                'message': 'This product is not in your cart'
            }
            return JsonResponse(data=data, status=500)

        self.user_cart.products.filter(product=self.product_obj).delete()
        return JsonResponse(data={}, status=200)


class SubmitOrder(LoginRequiredMixin, View):
    def get(self, request):
        if not self.request.user.cart.products.first():
            return redirect('index')
        if False in map(lambda x: x.product.is_available, self.request.user.cart.products.all()):
            return redirect('index')

        order_url = get_new_order_url()
        order = make_order(request, order_url)

        self.request.user.orders.add(order)
        self.request.user.cart.products.clear()
        return redirect('order', order.url)
