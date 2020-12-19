from django import forms
from django.forms import TextInput
from django.contrib.auth.models import User

from .models import Address


class SearchProductForm(forms.Form):
    query = forms.CharField()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'notify')
        labels = {
            'notify': 'Keep me notified on news and exclusive offers.'
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class AddressRegistrationForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('street', 'country', 'state', 'code')
        widgets = {
            'street': TextInput,
            'code': TextInput,
        }
