import json

from django.core.cache import cache

from cart.models import Category



class ContextMixin:

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        
        user = self.request.user
        user_auth = self.request.user.is_authenticated

        
        context['selected_page'] = int(self.request.GET.get("page")) if self.request.GET.get("page") else 1
        context['categories'] = cache.get_or_set('categories', Category.objects.all(), timeout=20)
        context['auth'] = int(user_auth)

        if user_auth:
            context['user_name'] = user.first_name or user.email

        if hasattr(self, "pages_count"):
            context['pages'] = list(range(1, self.pages_count + 1))

        if user_auth:
            user_cart = user.cart.all()
            context['user_cart'] = user_cart.select_related('product')

        return context



class Paginator:
    max_elements = 5

    def get_queryset(self, query=None):
        from math import ceil

        objects_count = query.count()
        pages_count: int = ceil(objects_count / Paginator.max_elements)
        self.pages_count = pages_count

        if self.request.GET.get("page"):
            page = int(self.request.GET.get("page"))

            if page > pages_count:
                page = pages_count
        else:
            page = 1

        start_object = page * Paginator.max_elements - Paginator.max_elements
        end_object = page * Paginator.max_elements
        return query[start_object:end_object]



def add_resent_by_cookie(request, product):
    
    resents = json.loads(request.COOKIES.get('resents') or '[]')

    # Update product position
    if product in resents:
        resents.remove(product)
    resents.append(product)

    return resents[-10:]
