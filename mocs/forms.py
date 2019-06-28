import datetime

from django import forms

from afol.models import Fan
from mocs.models import Moc, Vote, PublicVote


class MOCsForm(forms.ModelForm):
    year_built = forms.DateField(
        initial="1932-08-10",
        help_text="<ul><li>Only the year is important so entering yyyy-01-01 is acceptable.</li></ul>",
        widget=forms.SelectDateWidget(years=range(1932, datetime.date.today().year + 1),
                                      empty_label=("Choose Year", "Choose Month", "Choose Day")),
        required=True)

    year_retired = forms.DateField(
        initial="1932-08-10",
        help_text="<ul><li>Only the year is important so entering yyyy-01-01 is acceptable.</li>"
                  "<li>Only change if your MOC is no longer built otherwise leave the default value.</li>"
                  "<li>As long as the retired year is older than the year built it will not display.</li></ul>",
        widget=forms.SelectDateWidget(years=range(1932, datetime.date.today().year),
                                      empty_label=("Choose Year", "Choose Month", "Choose Day")),
        required=True)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MOCsForm, self).__init__(*args, **kwargs)
        self.fields['creator'].queryset = Fan.objects.filter(user=user)

    class Meta:
        model = Moc
        fields = ('creator', 'title', 'description', 'display_requirements', 'height', 'length',
                  'width', 'viewable_sides', 'url_photo', 'url_flickr',
                  'year_built', 'year_retired', 'is_public')


class PublicVoteForm(forms.ModelForm):

    class Meta:
        model = PublicVote
        fields = ('session', 'moc', 'category',)
        widgets = {'session': forms.HiddenInput,
                   'moc': forms.HiddenInput, 'category': forms.HiddenInput}


class FanVoteForm(forms.ModelForm):

    class Meta:
        model = Vote
        fields = ('fan', 'moc', 'category',)
        widgets = {'moc': forms.HiddenInput, 'category': forms.HiddenInput}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(FanVoteForm, self).__init__(*args, **kwargs)
        self.fields['fan'].queryset = Fan.objects.filter(user=user)

    def clean_fan(self):
        fan = self.cleaned_data['fan']
        category = self.cleaned_data.get("category")
        try:
            Vote.objects.get(fan=fan, category=category)
        except Vote.DoesNotExist:
            return fan
        raise forms.ValidationError("This fan already voted in this category.")
