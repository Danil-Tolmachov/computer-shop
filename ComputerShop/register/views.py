from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.contrib.auth.tokens import default_token_generator as token_generator


class Activation(View):

    def get(self, request, uidb64, token):
        User = get_user_model()
        print(uidb64, token)
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            print(token, uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and token_generator.check_token(user, token):
            print('changed', user.is_active)
            user.is_active = True
            print('changed', user.is_active)
            user.save()

            login(request, user)

        return redirect('index')
