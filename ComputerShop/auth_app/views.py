from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.core.exceptions import SuspiciousOperation, ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.views.generic import FormView

from auth_app.utils import send_change_password_email
from auth_app.validators import EmailValidator, PasswordValidator
from core.forms import LoginUserForm, CreateUserForm
from core.utils import ContextMixin
from auth_app.forms import EmailForm, RecoverPasswordForm
from auth_app.models import ShopUser
from cart.models import Product


# Account activation
class Activation(View):

    def get(self, request, uidb64: str, token: str):

        User = get_user_model()

        # Get user
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Activate user
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

        # Update last login
        self.request.user.last_login = timezone.now
        self.request.user.save()

        return reverse_lazy('index')


class CreateUser(ContextMixin, FormView):
    form_class = CreateUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('index')
    extra_context = {'title': 'Sign-up'}

    def form_valid(self, form):

        # Exclude extra data
        email = form.cleaned_data.pop('email')
        password = form.cleaned_data.pop('password1')
        password2 = form.cleaned_data.pop('password2')
        captcha = form.cleaned_data.pop('captcha')

        ShopUser.objects.create_user(email=email, password=password, **form.cleaned_data)

        return redirect('index')


class ChangeUser(View):
    success_url = 'account'

    def post(self, request):

        data = request.POST
        user = request.user

        # Set data
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

        # Validate changes
        try:
            EmailValidator.validate(request, password, 
                                    old_email=old_email, 
                                    new_email1=new_email1, 
                                    new_email2=new_email2,
                                )
        except SuspiciousOperation as err:
            return JsonResponse({'error': str(err)}, status=400)
            
        # Change data
        user.email = new_email1
        user.save()

        # Response
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

        # Validate changes
        try:
            PasswordValidator.validate(request, old_password, 
                                       new_password1=new_password1, 
                                       new_password2=new_password2,
                                    )
        except SuspiciousOperation as err:
            return JsonResponse({'error': str(err)}, status=400)
            
        # Change
        user.change_password(old_password, new_password1)

        return JsonResponse({}, status=200)


class ForgottenPassword(ContextMixin, FormView):
    form_class = EmailForm
    template_name = 'main/login.html'
    extra_context = {'title': 'Password Change'}
    success_url = reverse_lazy('index')

    def form_valid(self, form):

        user_model = get_user_model()
        username = form.cleaned_data['email']

        user = user_model.objects.get(email=username)

        # User check
        try:
            if user is None:
                return redirect('index')
        except:
            pass

        # Send message
        try:
            send_change_password_email(user, to_email=username)
        except:
            return redirect('forgot_password')

        return super().form_valid(form)


class RecoverPassword(FormView):
    form_class = RecoverPasswordForm
    template_name = 'main/login.html'
    extra_context = {'title': 'Set new password'}
    success_url = 'index'

    def form_valid(self, form):

        User = get_user_model()

        uidb64 = self.kwargs['uidb64']
        token = self.kwargs['token']

        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']

        if password1 != password2:
            raise ValueError('Passwords are the same')

        # Get user
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Change password
        if user is not None and token_generator.check_token(user, token):
            user.set_password(password1)
            user.save()

            login(self.request, user)

        return super().form_valid(form)


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

        # Validate comment
        try:
            self.validate_comment(content)
        except ValidationError as err:
            return JsonResponse({'error': err.message}, status=400)
            
        # Add comment
        product = self.get_product(product_id)
        product.add_comment(user, content, is_positive)

        return JsonResponse({}, status=200)

def logout_user(request):
    logout(request)
    return redirect('index')
