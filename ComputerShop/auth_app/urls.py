from django.urls import path

from auth_app.views import Activation, AddComment, ChangeEmail, ChangeUserPassword, LoginUser, CreateUser, ChangeUser, logout_user, Account, ForgotUserPassword

urlpatterns = [
    # Authentication system urls
    path('login/', LoginUser.as_view(), name='site-login'),
    path('logout/', logout_user, name='site-logout'),

    # Register and update user pathes
    path('register/', CreateUser.as_view(), name='register'),
    path('account/change-user', ChangeUser.as_view(), name='change_user'),
    path('account/change-email', ChangeEmail.as_view(), name='change_email'),
    path('account/change-password', ChangeUserPassword.as_view(), name='change_password'),
    path('forgot-password/', ForgotUserPassword.as_view(), name='forgot_password'),
    path('activation/<slug:uidb64>/<slug:token>/', Activation.as_view(), name='activate'),

    path('add-comment/', AddComment.as_view(), name='add_comment'),

    # Views
    path('account/', Account.as_view(), name='account'),


]
