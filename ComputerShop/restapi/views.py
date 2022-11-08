from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from cart.models import Product


class ProductsApiView(ListAPIView):
    queryset = Product.objects.all().values()

