from rest_framework import serializers

from cart.models import Product


class ProductListViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('pk', 'name', 'characteristics', 'price', 'is_available')
