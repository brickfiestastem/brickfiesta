from django.forms import ModelForm
from .models import CartItem


class ProfileForm(ModelForm):
    class Meta:
        model = CartItem
        fields = ('first_name', 'last_name', 'email')
