from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.views.generic import FormView, DetailView

from core.forms import LoginUserForm, CreateUserForm
from core.utils import ContextMixin
from register.forms import ChangeUserPasswordForm
from register.models import ShopUser


# Account activation
class Activation(View):

    def get(self, request, uidb64: str, token: str):
        User = get_user_model()

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.last_login = timezone.now()
            user.save()

            login(request, user)

        return redirect('index')


class LoginUser(ContextMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'
    extra_context = {'title': 'Login'}

    def get_success_url(self):
        self.request.user.last_login = timezone.now
        return reverse_lazy('index')


class CreateUser(ContextMixin, FormView):
    form_class = CreateUserForm
    template_name = 'main/register.html'
    success_url = ''
    extra_context = {'title': 'Sign-up'}

    def form_valid(self, form):
        email = form.cleaned_data.pop('email')
        password = form.cleaned_data.pop('password1')
        password2 = form.cleaned_data.pop('password2')
        captcha = form.cleaned_data.pop('captcha')

        ShopUser.objects.create_user(email=email, password=password, **form.cleaned_data)

        return redirect('index')


class ChangeUserPassword(ContextMixin, FormView):
    form_class = ChangeUserPasswordForm
    template_name = 'main/login.html'
    extra_context = {'title': 'Password Change'}

    def form_valid(self, form):
        username, password = form.cleaned_data['email'], form.cleaned_data['old_password']

        user = authenticate(username=username, password=password)
        login(request=self.request, user=user)

        if self.request.auth is not None:
            return redirect('change_password')

        if self.request.user.change_password(form.cleaned_data['old_password'], form.cleaned_data['new_password']):
            return reverse_lazy('index')
        else:
            logout(self.request)
            return redirect('change_password')


class Account(LoginRequiredMixin, ContextMixin, DetailView):
    model = ShopUser
    template_name = 'main/account.html'
    context_object_name = 'account'
    extra_context = {'title': 'Account'}

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        user = self.request.user

        context['account_buttons'] = [
            'Account settings',
        ]

        context['account_fields'] = {
            'First name': user.first_name,
            'Last name': user.last_name,
            'Country': user.country,
            'City': user.city,
            'Address': user.address,
            'Email': user.email,
            'Date joined': user.date_joined,
        }
        return context


def logout_user(request):
    logout(request)
    return redirect('index')