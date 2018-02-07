from django.forms import ModelForm
from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date', 'bricklink_username',
                  'twitter_handle', 'flickr_handle')
