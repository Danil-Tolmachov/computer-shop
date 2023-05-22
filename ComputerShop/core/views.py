from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Case, When
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from core.prefetch import prefetch_photos
from core.queries import filter_query_by_name_content, get_products_by_category

from cart.models import Product, Category, ProductImage
from core.utils import Paginator, ContextMixin, add_resent_by_cookie



class Index(Paginator, ContextMixin, ListView):
    model = Product
    product_image_model = ProductImage
    context_object_name = 'products'
    template_name = 'main/index.html'
    extra_context = {'title': 'ComputerShop'}

    def get_queryset(self):

        query = Product.objects.filter(is_visible=True)

        # Prefectching
        query = query.select_related('category').order_by('-pk')
        query = prefetch_photos(query)

        return query



class Catalog(Paginator, ContextMixin, ListView):
    model = Product
    category_model = Category
    product_image_model = ProductImage

    context_object_name = 'products'
    template_name = 'main/catalog.html'
    extra_context = {'title': 'Catalog'}


    def get_queryset(self, query=None):

        category = self.kwargs['category']
        
        if not self.kwargs and self.request.GET:
            query = Product.objects.filter(is_visible=True).order_by('-pk')
            query = super().get_queryset(query)

        # Category selection
        if category == 'all':
            query = self.model.objects.all()
        elif category:
            query = get_products_by_category(self.category_model, self.model, self.kwargs['category'])
        
        
        # Search selection
        if self.request.GET:
            content = self.request.GET['search']
            query = filter_query_by_name_content(query, content)

        # Prefetching
        query = query.select_related('category').order_by('-pk')
        query = prefetch_photos(query)

        return query



class ProductView(ContextMixin, DetailView):
    model = Product
    template_name = 'main/product.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'


    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.cookies_to_set = {}


    def get_object(self, *args, **kwargs):

        _object = super().get_object(*args, **kwargs)

        # Add product to resents
        if self.request.user.is_authenticated:
            user = self.request.user

            user.resents = user.get_added_resents(_object.pk)
            user.save(update_fields=["resents"])
            
        else:
            self.resents = add_resent_by_cookie(self.request, _object.pk)
            self.cookies_to_set['resents'] = self.resents

        self.comments = _object.get_comments()

        return _object


    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)

        # Use db cookies if autheticated
        if self.request.user.is_authenticated:
            resents_list = self.request.user.get_resents()
        else:
            resents_list = self.resents

        # Get resents products
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(resents_list)])
        resents_query = Product.objects.filter(pk__in=resents_list).order_by(preserved)
        context['resents'] = resents_query

        # Get comments
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(self.comments)])
        context['comments'] = self.comments

        context['title'] = Product.objects.only('pk', 'name').get(pk=self.kwargs['product_id']).name

        return context


    def render_to_response(self, context, **response_kwargs):

        response = super(ProductView, self).render_to_response(context, **response_kwargs)

        # Set cookies
        for key, cookie in self.cookies_to_set.items():
            response.set_cookie(key, cookie)

        return response



class Account(LoginRequiredMixin, ContextMixin, DetailView):
    model = get_user_model()
    template_name = 'main/account/account.html'
    context_object_name = 'account'
    extra_context = {'title': 'Account'}

    def __init__(self, **kwargs: Any) -> None:
        return super().__init__(**kwargs)


    def get_object(self, queryset=None):
        return self.request.user


    def get_context_data(self, *, object_list=None, **kwargs):
        # How to add new page to account page:
        # 
        # 1. Extend context['account_buttons'] with new button
        # 2. Create template and extend context['account_pages'] with path to template

        context = super().get_context_data(object_list=object_list, **kwargs)

        user = self.request.user
        active_orders = user.orders.filter(is_closed=False)
        archive_orders = user.orders.filter(is_closed=True)

        # Prefetching
        active_orders = active_orders.prefetch_related('products', 'products__product__category')
        archive_orders = archive_orders.prefetch_related('products', 'products__product__category')

        # Sidebar buttons
        context['account_buttons'] = [
            'Account settings', 
            'Active orders', 
            'Order history',
            'Change password',
            'Change email', 
        ]

        # Pathes to included content
        context['account_pages'] = [
            'main/account/account_settings.html',
            'main/account/active_orders.html',
            'main/account/archive_orders.html',
            'main/account/change_password.html',
            'main/account/change_email.html',
        ]

        # Account settings fields
        context['account_fields'] = {
            'First name': {'value': user.first_name, 'is_changeable': True},
            'Last name': {'value': user.last_name, 'is_changeable': True},
            'Country': {'value': user.country, 'is_changeable': True},
            'City': {'value': user.city, 'is_changeable': True},
            'Address': {'value': user.address, 'is_changeable': True},
            'Email': {'value': user.email, 'is_changeable': False},
            'Date joined': {'value': user.date_joined, 'is_changeable': False},
        }

        # Orders context
        context['active_orders'] = dict(enumerate(active_orders))
        context['archive_orders'] = dict(enumerate(archive_orders))

        return context



def about_us(request):
    template_name = 'main/about_us.html'
    context = {'title': 'About-us'}
    return render(request, template_name=template_name, context=context)
