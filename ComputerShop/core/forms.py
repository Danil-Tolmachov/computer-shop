from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from auth_app.models import ShopUser


class LoginUserForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = forms.EmailInput(
            attrs={'class': 'field', 'placeholder': ''}
        )

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'field',
            'placeholder': '',
        }
    ))


class CreateUserForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)


    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'field',
            'placeholder': 'Password',
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'field',
            'placeholder': 'Password Confirmation',
        })


    class Meta:
        model = ShopUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'country', 'city', 'address', 'captcha']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'field',
                'placeholder': 'First Name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'field',
                'placeholder': 'Last Name',
            }),
            'email': forms.TextInput(attrs={
                'class': 'field',
                'placeholder': 'Email',
            }),
            'country': forms.TextInput(attrs={
                'class': 'field',
                'placeholder': 'Country',
            }),
            'city': forms.TextInput(attrs={
                'class': 'field',
                'placeholder': 'City',
            }),
            'address': forms.TextInput(attrs={
                'class': 'field',
                'placeholder': 'Address',
            }),
        }
