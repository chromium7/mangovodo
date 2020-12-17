from django import forms

from shop.models import Address

from .models import Order


class OrderCreateForm(forms.ModelForm):
    address = forms.ModelChoiceField(
        widget=forms.RadioSelect,
        queryset=None,
        empty_label=None,
        label='Select your address for shipping',
    )

    class Meta:
        model = Order
        fields = ['address']
        exclude = ['buyer']

    def __init__(self, user, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.fields['address'].queryset = Address.objects.filter(user=user)
