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
        user.profile.birth_date = self.cleaned_data["birth_date"]
        user.profile.bricklink_username = self.cleaned_data["bricklink_username"]
        user.profile.twitter_handle = self.cleaned_data["twitter_handle"]
        user.profile.flickr_handle = self.cleaned_data["flickr_handle"]
        if commit:
            user.save()
            user.profile.save()
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
