from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User
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

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'birth_date')


class AfolUserChangeForm(forms.ModelForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    birth_date = forms.DateField(
        help_text="<ul><li>Only the year is important so entering yyyy-01-01 is acceptable.</li></ul>",
        widget=forms.SelectDateWidget(years=range(1932, datetime.date.today().year),
                                      empty_label=("Choose Year", "Choose Month", "Choose Day")),
        required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'birth_date', 'bricklink_username', 'twitter_handle', 'flickr_handle')
