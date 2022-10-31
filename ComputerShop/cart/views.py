from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from cart.models import Product, Cart
from core.utils import ContextMixin


class CartView(LoginRequiredMixin, ContextMixin, DetailView):
    model = Cart
    template_name = "main/cart.html"
    context_object_name = 'cart'

    # Get current user cart object method
    def get_object(self, queryset=None):
        return self.request.user.cart.pk


class CartItemAdd(View):

    @csrf_exempt
    def post(self, request):
        self.item_id = int(request.POST['id'])
        self.product_obj = Product.objects.get(pk=self.item_id)

        if self.product_obj not in request.user.cart.products.all():
            request.user.cart.products.add(self.product_obj)

            # item container context
            data = {
                'pk': self.product_obj.pk,
                'name': self.product_obj.name,
            }

            return JsonResponse(data=data, status=200)
        else:
            data = {
                'message': 'This product is already in your cart'
            }
            return JsonResponse(data=data, status=500)


class CartItemDelete(View):

    @csrf_exempt
    def post(self, request):
        self.item_id = int(request.POST['id'])

        if Product.objects.get(pk=self.item_id):
            self.product_obj = Product.objects.get(pk=self.item_id)
        else:
            data = {
                'message': 'This product is not in your cart'
            }
            return JsonResponse(data=data, status=500)

        request.user.cart.products.remove(self.product_obj)
        return JsonResponse(data={}, status=200)
