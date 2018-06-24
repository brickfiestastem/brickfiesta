import datetime

from django import forms

from afol.models import Fan
from mocs.models import Moc


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
        fields = ('creator', 'title', 'description', 'height', 'length',
                  'width', 'viewable_sides', 'url_photo', 'url_flickr',
                  'year_built', 'year_retired', 'is_public')
