from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import (
        AuthenticationForm,
        UserCreationForm,
        PasswordResetForm,
        )
from django.contrib.auth.models import User
from django import forms
from tokens.models import AccountActivationToken

class UsernameField(forms.CharField):
    def to_python(self, value):
        return value.lower()

class LogInForm(AuthenticationForm):
    username = UsernameField(label='Username')
    password = forms.CharField(label='Password',
                            widget=forms.PasswordInput())

class CreateAccountForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super(CreateAccountForm, self).clean()
        if not cleaned_data:
            raise forms.ValidationError('You must fill out all the fields!')
        try:
            if '@fiu.edu' not in cleaned_data['email']:
                self._errors['email'] = ['Only FIU Emails are allowed!']
                del cleaned_data['email']
            else:
                if User.objects.filter(username=cleaned_data['email'].split('@')[0]).exists():
                    reset_link = "<a href='" + reverse('password_reset') + "'>here</a>"
                    self._errors['email'] = [mark_safe("There is already an account with this email address! If you've forgotten your login info please reset your password " + reset_link)]
        except KeyError:
            raise forms.ValidationError('You are missing the email field!')
        return cleaned_data

    def save(self, commit=True):
        user = super(CreateAccountForm,self).save(commit=False)
        user.username = user.email.split('@')[0].lower()
        user.is_active = False
        if commit:
            user.save()
        return user

class ActivateAccountForm(forms.ModelForm):
    class Meta:
        model = AccountActivationToken
        fields = []

class ForgotPasswordForm(PasswordResetForm):
    pass
