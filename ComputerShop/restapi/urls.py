from django.urls import path, include, re_path
from rest_framework import routers

from restapi.views import ProductsApiViewSet

product_router = routers.DefaultRouter()
product_router.register(r'product', ProductsApiViewSet, basename='product')


urlpatterns = [
    path('', include(product_router.urls), name='api_index'),

    path('auth/', include('djoser.urls'), name='api_djoser'),
    re_path('auth/', include('djoser.urls.authtoken'), name='api_login')  # LoginApiView.as_view(), name='api_login')
]
