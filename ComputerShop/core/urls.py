from django.urls import path, include
from django.views.decorators.cache import cache_page

from core.views import Index, about_us, Catalog, ProductView

urlpatterns = [
    #  Include apps
    path('', include('cart.urls')),
    path('', include('register.urls')),

    #  Api
    path('api/', include('restapi.urls')),

    #  Views
    path('', Index.as_view(), name='index'),
    path('catalog/<slug:category>/', Catalog.as_view(), name='catalog'),
    path('product/<int:product_id>/', ProductView.as_view(), name='product'),
    path('about-us/', about_us, name='about_us'),

]
