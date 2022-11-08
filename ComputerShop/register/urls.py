from django.urls import path

from register.views import Activation, LoginUser, CreateUser, logout_user, Account

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', CreateUser.as_view(), name='register'),
    path('account/', Account.as_view(), name='account'),

    path('activation/<slug:uidb64>/<slug:token>/', Activation.as_view(), name='activate')
]
