from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.datastructures import MultiValueDictKeyError
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView
from core.prefetch import prefetch_photos

from cart.models import Product, ProductItem, Order
from cart.utils import make_order, get_new_order_url
from core.utils import ContextMixin


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
        return self.request.user.orders.filter(is_closed=False).prefetch_related('products')


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
        item_id = int(request.POST['id'])
        product_obj = Product.objects.get(pk=item_id)

        user_cart = request.user.cart

        # if selected product not in user cart products
        if product_obj not in map(lambda x: x.product, user_cart.all()):
            item = ProductItem.objects.create(product=product_obj, product_count=1)

            request.user.cart.add(item)

            # item container context
            data = {
                'pk': product_obj.pk,
                'name': product_obj.name,
            }

            return JsonResponse(data=data, status=200)
        # else add 1 to product count
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

        try:
            item_count = int(request.POST['count'])
        except MultiValueDictKeyError:
            item_count = 1

        user_cart = request.user.cart

        user_product = user_cart.filter(product=product_obj)
        user_product.update(product_count=item_count)

        data = {
            'summary': request.user.get_cart_summary()
        }
        return JsonResponse(data=data, status=200)


class CartItemDelete(View):

    @csrf_exempt
    def post(self, request):
        item_id = int(request.POST['id'])
        user_cart = request.user.cart

        if Product.objects.get(pk=item_id) in map(lambda x: x.product, user_cart.all()):
            product_obj = Product.objects.get(pk=item_id)
        else:
            data = {
                'error': 'This product is not in your cart'
            }
            return JsonResponse(data=data, status=500)

        user_cart.filter(product=product_obj).delete()
        return JsonResponse(data={}, status=200)


class SubmitOrder(LoginRequiredMixin, View):
    def get(self, request):
        if not self.request.user.cart.first():
            return redirect('index')
        if False in map(lambda x: x.product.is_available, self.request.user.cart.all()):
            return redirect('index')

        order_url = get_new_order_url()
        order = make_order(request, order_url)

        self.request.user.orders.add(order)
        self.request.user.cart.clear()
        return redirect('order', order.url)
