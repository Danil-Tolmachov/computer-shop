from django.urls import path

from register.views import Activation, LoginUser, CreateUser, logout_user, Account, ChangeUserPassword

urlpatterns = [
    # Authentication system urls
    path('login/', LoginUser.as_view(), name='site-login'),
    path('logout/', logout_user, name='site-logout'),

    # Register and change user
    path('register/', CreateUser.as_view(), name='register'),
    path('forgot-password/', ChangeUserPassword.as_view(), name='change_password'),
    path('activation/<slug:uidb64>/<slug:token>/', Activation.as_view(), name='activate'),

    # Views
    path('account/', Account.as_view(), name='account'),


]
