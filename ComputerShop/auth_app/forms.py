from django import forms

from auth_app.models import ShopUser


class ChangeUserPasswordForm(forms.Form):
    email = forms.EmailField()
    old_password = forms.CharField(max_length=255)
    new_password = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super(ChangeUserPasswordForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'field', 'placeholder': 'Email address'}
        )
        self.fields['old_password'].widget = forms.PasswordInput(
            attrs={'class': 'field', 'placeholder': 'Old password'}
        )
        self.fields['new_password'].widget = forms.PasswordInput(
            attrs={'class': 'field', 'placeholder': 'New password'}
        )

class ChangeUserForm(forms.ModelForm):
    
    class Meta:
        model = ShopUser
        exclude = ('email', 'password')
