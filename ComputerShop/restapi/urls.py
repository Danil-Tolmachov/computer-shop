from django.urls import path, include, re_path
from rest_framework import routers

from restapi.views import ProductsApiViewSet

#  Routers
product_router = routers.DefaultRouter()
product_router.register(r'product', ProductsApiViewSet, basename='product')


urlpatterns = [
    #  Views
    path('', include(product_router.urls), name='api_index'),

    #  Djoser
    path('auth/', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.authtoken'))  # LoginApiView.as_view(), name='api_login')
]
