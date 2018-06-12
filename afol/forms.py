from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Shirt, Fan
from event.models import Event
import datetime


class AfolUserCreateForm(UserCreationForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    birth_date = forms.DateField(
        initial="1932-08-10",
        help_text="<ul><li>Only the year is important so entering yyyy-01-01 is acceptable.</li></ul>",
        widget=forms.SelectDateWidget(years=range(1932, datetime.date.today().year),
                                      empty_label=("Choose Year", "Choose Month", "Choose Day")),
        required=True)
    bricklink_username = forms.CharField(required=False)
    flickr_handle = forms.CharField(required=False)
    twitter_handle = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email


class AfolUserChangeForm(forms.ModelForm):
    birth_date = forms.DateField(
        initial="1932-08-10",
        help_text="<ul><li>Only the year is important so entering yyyy-01-01 is acceptable.</li></ul>",
        widget=forms.SelectDateWidget(years=range(1932, datetime.date.today().year),
                                      empty_label=("Choose Year", "Choose Month", "Choose Day")),
        required=True)
    bricklink_username = forms.CharField(required=False)
    flickr_handle = forms.CharField(required=False)
    twitter_handle = forms.CharField(required=False)

    class Meta:
        model = Profile
        fields = {'birth_date', 'bricklink_username',
                  'flickr_handle', 'twitter_handle'}


class ShirtChangeForm(forms.ModelForm):

    class Meta:
        model = Shirt
        fields = ['fan', 'event', 'shirt_size']
        widgets = {
            'fan': forms.HiddenInput(),
            'event': forms.HiddenInput(),
        }
