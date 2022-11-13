from ComputerShop.settings import MEDIA_URL
from cart.models import Category, Product


class ContextMixin:

    def get_context_data(self, *, object_list=None, **kwargs):
        user = self.request.user

        context = super().get_context_data(**kwargs)
        context['selected_page'] = int(self.request.GET.get("page")) if self.request.GET.get("page") else 0
        context['categories'] = Category.objects.all()
        context['MEDIA_URL'] = MEDIA_URL

        if str(user) != "AnonymousUser":
            context['user_name'] = user.first_name if user.first_name else user.email

        else:
            context['user_name'] = str(user)

        if hasattr(self, "pages_count"):
            context['pages'] = list(range(1, self.pages_count + 1))

        if str(user) != "AnonymousUser":
            user_cart = user.cart.all()
            context['cart'] = user_cart.all()

        return context


class Paginator(ContextMixin):
    max_elements = 5

    def get_queryset(self, query=None):
        from math import ceil

        objects = query.count()
        self.pages_count = ceil(objects / Paginator.max_elements)

        if self.request.GET.get("page"):
            page = int(self.request.GET.get("page"))

            if page > self.pages_count:
                page = 1
        else:
            page = 1

        start_object = page * Paginator.max_elements - Paginator.max_elements
        end_object = page * Paginator.max_elements

        return query[start_object:end_object]