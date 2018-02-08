from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    birth_date = forms.DateField()
    bricklink_username = forms.CharField(max_length=64, blank=True)
    twitter_handle = forms.CharField(max_length=64, blank=True)
    flickr_handle = forms.CharField(max_length=128, blank=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'birth_date', 'bricklink_username',
                  'twitter_handle', 'flickr_handle')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date', 'bricklink_username',
                  'twitter_handle', 'flickr_handle')
