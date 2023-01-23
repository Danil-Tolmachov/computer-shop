from django import forms


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


class RecoverPasswordForm(forms.Form):
    password1 = forms.CharField(max_length=255)
    password2 = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super(RecoverPasswordForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'field', 'placeholder': 'New password'}
        )
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'field', 'placeholder': 'New password confirmation'}
        )
    
    class Meta:
        fields = ('password1', 'password2')


class EmailForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'field', 'placeholder': 'Email address'}
        )
    
    class Meta:
        fields = ('email',)
