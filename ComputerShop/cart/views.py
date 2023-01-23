from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.datastructures import MultiValueDictKeyError
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.decorators.csrf import csrf_exempt
from core.prefetch import prefetch_photos
from django.shortcuts import redirect

from cart.models import Product, ProductItem, Order
from core.utils import ContextMixin
from cart.utils import get_new_order_url



class CartView(LoginRequiredMixin, ContextMixin, DetailView):
    template_name = "main/cart.html"
    context_object_name = 'cart'
    extra_context = {'title': 'Cart'}

    def get_object(self, queryset=None):

        query = self.request.user.cart.all()

        # Prefetching
        query = query.prefetch_related('product')
        query = prefetch_photos(query, nested_prefetch='product__')
        
        return query


class OrderListView(ContextMixin, ListView):
    model = Order
    template_name = "main/orders.html"
    context_object_name = 'orders'
    extra_context = {'title': 'Orders'}

    def get_queryset(self):
        _active_orders = self.request.user.orders.filter(is_closed=False)
        return _active_orders.prefetch_related('products')


class OrderView(ContextMixin, DetailView):
    model = Order
    template_name = "main/order.html"
    context_object_name = 'order'
    extra_context = {'title': 'Order tracker'}

    def get_object(self, queryset=None):

        order_id = self.kwargs['order_url']
        order = self.model.objects.get(url=order_id)

        return order


class CartItemAdd(View):


    @csrf_exempt
    def post(self, request):

        item_id = int(request.POST['id'])
        product_obj = Product.objects.get(pk=item_id)

        user_cart = request.user.cart

        # If selected product not in user cart products
        if product_obj not in map(lambda x: x.product, user_cart.all()):
            item = ProductItem.objects.create(product=product_obj, product_count=1)

            request.user.cart.add(item)

            # item container context
            data = {
                'pk': product_obj.pk,
                'name': product_obj.name,
            }

            return JsonResponse(data=data, status=200)

        # Else add 1 to product count
        else:
            user_product = user_cart.filter(product=product_obj)
            user_product.update(product_count=user_product.first().product_count+1)

            data = {

            }
            return JsonResponse(data=data, status=304)

class CartItemSet(View):


    @csrf_exempt
    def post(self, request):

        item_id = int(request.POST['id'])
        product_obj = Product.objects.get(pk=item_id)

        # Get count
        try:
            item_count = int(request.POST['count'])
        except MultiValueDictKeyError:
            item_count = 1

        user_cart = request.user.cart

        # Update cart
        user_product = user_cart.filter(product=product_obj)
        user_product.update(product_count=item_count)

        # Response data
        data = {
            'summary': request.user.get_cart_summary()
        }

        return JsonResponse(data=data, status=200)


class CartItemDelete(View):
    product_model = Product

    @csrf_exempt
    def post(self, request):

        item_id = int(request.POST['id'])
        user_cart = request.user.cart

        product = self.product_model.objects.get(pk=item_id)
        cart_products = map(lambda x: x.product, user_cart.all())

        # Delete product from cart
        if product in cart_products:

            user_cart.filter(product=product_obj).delete()

        else:
            data = {
                'error': 'This product is not in your cart'
            }

            return JsonResponse(data=data, status=500)

        return JsonResponse(data={}, status=200)


class SubmitOrder(LoginRequiredMixin, View):


    def get(self, request):
    
        # If cart is empty
        if not self.request.user.cart.first():
            return redirect('index')

        # If not available product in cart
        if False in map(lambda x: x.product.is_available, self.request.user.cart.all()):
            return redirect('index')

        order_url = get_new_order_url()
        order = request.user.get_order(request, order_url)

        # Move cart products to order
        self.request.user.orders.add(order)
        self.request.user.cart.clear()

        return redirect('order', order.url)
