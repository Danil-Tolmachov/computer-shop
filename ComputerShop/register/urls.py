from django.urls import path

from register.views import Activation

urlpatterns = [
    path('activation/<slug:uidb64>/<slug:token>/', Activation.as_view(), name='activate')
]
