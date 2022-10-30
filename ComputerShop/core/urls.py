from django.urls import path, include

from core.views import Index, about_us, Catalog, ProductView, LoginUser, CreateUser, Account, logout_user

urlpatterns = [
    # Authentication system urls
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', CreateUser.as_view(), name='register'),
    path('account/', Account.as_view(), name='account'),

    # include other apps
    path('', include('cart.urls')),
    path('', include('register.urls')),

    # Staff urls
    # path('profile/<int:user_id>/', Profile.as_view(), name='profile'),

    # Views
    path('', Index.as_view(), name='index'),
    path('catalog/<slug:category>/', Catalog.as_view(), name='catalog'),
    path('product/<int:product_id>/', ProductView.as_view(), name='product'),
    path('about-us/', about_us, name='about_us'),

]
