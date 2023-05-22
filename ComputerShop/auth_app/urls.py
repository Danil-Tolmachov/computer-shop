from django.urls import path

from auth_app.views import Activation, AddComment, ChangeEmail, ForgottenPassword, RecoverPassword, ChangeUserPassword, LoginUser, CreateUser, ChangeUser, logout_user

urlpatterns = [
    # Authentication system urls
    path('login/', LoginUser.as_view(), name='user-login'),
    path('logout/', logout_user, name='user-logout'),

    path('register/', CreateUser.as_view(), name='register'),
    path('activation/<slug:uidb64>/<slug:token>/', Activation.as_view(), name='activate'),

    # JSON responses
    path('account/change-user', ChangeUser.as_view(), name='change_user'),
    path('account/change-email', ChangeEmail.as_view(), name='change_email'),
    path('account/change-password', ChangeUserPassword.as_view(), name='change_password'),

    # Password recovery
    path('change-password/<slug:uidb64>/<slug:token>/', RecoverPassword.as_view(), name='change_forgotten_password'),
    path('forgot-password/', ForgottenPassword.as_view(), name='forgot_password'),

    # Other actions
    path('add-comment/', AddComment.as_view(), name='add_comment'),
]
