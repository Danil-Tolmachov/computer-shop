from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import SuspiciousOperation, ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.views.generic import FormView, DetailView
from django.db.models import Prefetch
from auth_app.validators import EmailValidator, PasswordValidator

from core.forms import LoginUserForm, CreateUserForm
from core.utils import ContextMixin
from auth_app.forms import ChangeUserForm, ChangeUserPasswordForm
from auth_app.models import ShopUser
from cart.models import Product


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


class ChangeUser(View):
    form_class = ChangeUserForm
    success_url = 'account'

    def post(self, request):
        data = request.POST
        user = request.user

        user.first_name = data['First name'] or user.first_name
        user.last_name = data['Last name'] or user.last_name
        user.country = data['Country'] or user.country
        user.city = data['City'] or user.city
        user.address = data['Address'] or user.address

        user.save()

        return redirect(self.success_url)


class ChangeEmail(View):
    success_url = 'account'

    def post(self, request):

        data = request.POST
        user = request.user

        password = data['password']
        old_email = request.user.email
        new_email1 = data['new_email1']
        new_email2 = data['new_email2']


        try:
            EmailValidator.validate(request, password, 
                                    old_email=old_email, 
                                    new_email1=new_email1, 
                                    new_email2=new_email2,
                                )
        except SuspiciousOperation as err:
            return JsonResponse({'error': str(err)}, status=400)
            
        
        user.email = new_email1
        user.save()

        response_data = {
            'new_email': user.email
        }

        return JsonResponse(response_data,status=200)


class ChangeUserPassword(View):
    success_url = 'account'

    def post(self, request):
        data = request.POST
        user = request.user

        old_password = data['password']
        new_password1 = data['new_password1']
        new_password2 = data['new_password2']


        try:
            PasswordValidator.validate(request, old_password, 
                                       new_password1=new_password1, 
                                       new_password2=new_password2,
                                    )
        except SuspiciousOperation as err:
            return JsonResponse({'error': str(err)}, status=400)
            
        
        user.change_password(old_password, new_password1)

        return JsonResponse({}, status=200)


class ForgotUserPassword(ContextMixin, FormView):
    form_class = ChangeUserPasswordForm
    template_name = 'main/login.html'
    extra_context = {'title': 'Password Change'}

    def form_valid(self, form):
        username, password = form.cleaned_data['email'], form.cleaned_data['old_password']

        user = authenticate(username=username, password=password)
        login(request=self.request, user=user)

        try:
            if self.request.auth is not None:
                return redirect('change_password')
        except:
            return redirect('change_password')

        if self.request.user.change_password(form.cleaned_data['old_password'], form.cleaned_data['new_password']):
            return reverse_lazy('index')
        else:
            logout(self.request)
            return redirect('change_password')


class Account(LoginRequiredMixin, ContextMixin, DetailView):
    model = ShopUser
    template_name = 'main/account/account.html'
    context_object_name = 'account'
    extra_context = {'title': 'Account'}

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        How to add new page to account page:

        1. Extend context['account_buttons'] with new button
        2. Create template and extend context['account_pages'] with path to template
        """
        context = super().get_context_data(object_list=object_list, **kwargs)

        user = self.request.user
        active_orders = user.orders.filter(is_closed=False)
        archive_orders = user.orders.filter(is_closed=True)

        # Prefetching
        active_orders = active_orders.prefetch_related('products', 'products__product__category')
        archive_orders = archive_orders.prefetch_related('products', 'products__product__category')

        context['account_buttons'] = [
            'Account settings', 
            'Active orders', 
            'Order history',
            'Change password',
            'Change email', 
        ]

        # Pages pathes to included content
        context['account_pages'] = [
            'main/account/account_settings.html',
            'main/account/active_orders.html',
            'main/account/archive_orders.html',
            'main/account/change_password.html',
            'main/account/change_email.html',
        ]

        context['account_fields'] = {
            'First name': {'value': user.first_name, 'is_changeable': True},
            'Last name': {'value': user.last_name, 'is_changeable': True},
            'Country': {'value': user.country, 'is_changeable': True},
            'City': {'value': user.city, 'is_changeable': True},
            'Address': {'value': user.address, 'is_changeable': True},
            'Email': {'value': user.email, 'is_changeable': False},
            'Date joined': {'value': user.date_joined, 'is_changeable': False},
        }

        context['active_orders'] = dict(enumerate(active_orders))

        context['archive_orders'] = dict(enumerate(archive_orders))

        return context

class AddComment(View):
    product_model = Product

    def get_product(self, id):
        return self.product_model.objects.get(pk=id)

    def validate_comment(self, content):
        if content == '':
            raise ValidationError("You can't post an empty comment")

    def post(self, request):
        data = request.POST
        user = request.user

        product_id: int = data['product']
        content: str = data['content']
        is_positive: bool = data['is_positive'] == str(1)

        try:
            self.validate_comment(content)
        except ValidationError as err:
            return JsonResponse({'error': err.message}, status=400)
            
        product = self.get_product(product_id)
        product.add_comment(user, content, is_positive)

        return JsonResponse({}, status=200)

def logout_user(request):
    logout(request)
    return redirect('index')
