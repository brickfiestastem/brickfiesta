from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class AfolUserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields


class AfolUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields
