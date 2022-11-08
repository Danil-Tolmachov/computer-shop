from django.urls import path

from restapi.views import ProductsApiView

urlpatterns = [
    path('', ProductsApiView.as_view(), name='api_index')
]
