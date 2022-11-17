from django.urls import path, include
from rest_framework import routers

from restapi.views import ProductsApiViewSet, ShopUserAPIViewSet, LoginApiView

product_router = routers.DefaultRouter()
product_router.register(r'product', ProductsApiViewSet, basename='product')


urlpatterns = [
    path('', include(product_router.urls), name='api_index'),

    path('users/', ShopUserAPIViewSet.as_view({'get': 'list_user'}), name='api_users'),
    path('users/<int:user_id>/', ShopUserAPIViewSet.as_view({'get': 'detail_user'}), name='api_user'),
    path('users/<int:user_id>/', ShopUserAPIViewSet.as_view({'put': 'put'}), name='api_put_user'),
    path('users/<int:user_id>/', ShopUserAPIViewSet.as_view({'delete': 'delete'}), name='api_delete_user'),

    path('auth/', include('djoser.urls.authtoken'), name='api_login')  # LoginApiView.as_view(), name='api_login')
]
