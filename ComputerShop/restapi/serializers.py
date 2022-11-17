from rest_framework import serializers

from cart.models import Product
from register.models import ShopUser


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('pk', 'name', 'characteristics', 'price', 'is_available')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopUser
        fields = ('pk', 'first_name', 'last_name',
                  'country', 'city', 'address',
                  'email',
                  'cart', 'orders',
                  'resents', 'notifications',
                  'date_joined', 'is_active'
                  )


class UserUpdateSerializer(serializers.ModelSerializer):
    cart = serializers.JSONField(allow_null=True, required=False)
    orders = serializers.JSONField(allow_null=True, required=False)
    is_active = serializers.BooleanField(allow_null=True, required=False, default=None)
    email = serializers.EmailField(max_length=255, required=False)

    class Meta:
        model = ShopUser
        fields = ('pk', 'first_name', 'last_name',
                  'country', 'city', 'address',
                  'email',
                  'cart', 'orders',
                  'resents', 'notifications',
                  'date_joined', 'is_active'
                  )


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password1 = serializers.CharField(max_length=255)

    # def create(self, **validated_data):
    #     user = ShopUser.objects.create_user(validated_data.pop('email'),
    #                                         validated_data.pop('password'),
    #                                         **validated_data)
    #     return user
