from django import forms
from .models import CartItem


class CartItemForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = CartItem
        fields = ('first_name', 'last_name', 'email')
