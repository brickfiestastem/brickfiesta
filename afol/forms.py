from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class AfolUserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'birth_date')


class AfolUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'birth_date', 'bricklink_username', 'twitter_handle', 'flickr_handle')
