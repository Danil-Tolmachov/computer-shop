from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, FormView

from cart.models import Product, Category
from core.forms import LoginUserForm, CreateUserForm
from core.utils import Paginator, ContextMixin
from register.models import ShopUser


class Index(Paginator, ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'main/index.html'

    def get_queryset(self, query=None):
        query = Product.objects.filter(is_visible=True).order_by('-pk')
        query = super().get_queryset(query)

        return query


class Catalog(Paginator, ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'main/catalog.html'

    def get_queryset(self, query=None):
        if self.kwargs:
            if not Category.objects.filter(category_name=self.kwargs['category']):
                return []
            query = Product.objects.filter(
                category=Category.objects.filter(category_name=self.kwargs['category'])[0].pk
            )
            query = super().get_queryset(query)
            return query

        query = Product.objects.filter(is_visible=True).order_by('-pk')
        query = super().get_queryset(query)

        return query


class ProductView(ContextMixin, DetailView):
    model = Product
    template_name = 'main/product.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'


class LoginUser(ContextMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_success_url(self):
        self.request.user.last_login = timezone.now
        return reverse_lazy('index')


class CreateUser(ContextMixin, FormView):
    form_class = CreateUserForm
    template_name = 'main/register.html'
    success_url = ''

    def form_valid(self, form):
        email = form.cleaned_data.pop('email')
        password = form.cleaned_data.pop('password1')
        password2 = form.cleaned_data.pop('password2')

        ShopUser.objects.create_user(email=email, password=password, **form.cleaned_data)

        return redirect('index')


class Account(LoginRequiredMixin, ContextMixin, DetailView):
    model = ShopUser
    template_name = 'main/account.html'

    def get_object(self, queryset=None):
        return self.request.user


def logout_user(request):
    logout(request)
    return redirect('index')


def about_us(request):
    template_name = 'main/about_us.html'
    return render(request, template_name=template_name)
