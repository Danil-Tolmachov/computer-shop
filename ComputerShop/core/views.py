from django.db.models import Prefetch, Case, When
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from cart.models import Product, Category, ProductImage
from core.utils import Paginator, ContextMixin


class Index(Paginator, ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'main/index.html'
    extra_context = {'title': 'ComputerShop'}

    def get_queryset(self, query=None):
        query = Product.objects.filter(is_visible=True).select_related('category').order_by("pk")
        prefetch = Prefetch('images', queryset=ProductImage.objects.distinct(), to_attr='photo')

        query = super().get_queryset(query.prefetch_related(prefetch))
        return reversed(query)


class Catalog(Paginator, ListView):
    model = Product
    category_model = Category

    context_object_name = 'products'
    template_name = 'main/catalog.html'
    extra_context = {'title': 'Catalog'}

    def get_queryset(self, query=None):
        if self.kwargs:
            category = self.category_model.objects.get(category_slug=self.kwargs['category'])

            query = self.model.objects.filter(category=category.pk)

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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        resents_list = self.request.user.get_resents()

        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(resents_list)])
        resents_query = Product.objects.filter(pk__in=resents_list).order_by(preserved)

        context['resents'] = resents_query
        context['title'] = Product.objects.get(pk=self.kwargs['product_id']).name
        return context

    def get_object(self, *args, **kwargs):
        _object = super().get_object(*args, **kwargs)
        user = self.request.user

        user.resents = user.get_added_resents(_object.pk)
        user.save(update_fields=["resents"])

        return _object


def about_us(request):
    template_name = 'main/about_us.html'
    context = {'title': 'About-us'}
    return render(request, template_name=template_name, context=context)
