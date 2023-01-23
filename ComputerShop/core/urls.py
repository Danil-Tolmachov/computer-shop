from django.urls import path, include

from core.views import Account, Index, about_us, Catalog, ProductView

urlpatterns = [
    #  Include apps
    path('', include('cart.urls')),
    path('', include('auth_app.urls')),

    #  Pages
    path('', Index.as_view(), name='index'),
    path('catalog/<slug:category>/', Catalog.as_view(), name='catalog'),
    path('product/<int:product_id>/', ProductView.as_view(), name='product'),
    path('account/', Account.as_view(), name='account'),

    path('about-us/', about_us, name='about_us'),

]
