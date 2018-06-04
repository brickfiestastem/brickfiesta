from django import forms
from mocs.models import Moc
import datetime


class MOCsForm(forms.ModelForm):
    year_built = forms.DateField(
        initial="1932-08-10",
        help_text="<ul><li>Only the year is important so entering yyyy-01-01 is acceptable.</li></ul>",
        widget=forms.SelectDateWidget(years=range(1932, datetime.date.today().year),
                                      empty_label=("Choose Year", "Choose Month", "Choose Day")),
        required=True)

    year_retired = forms.DateField(
        initial="1932-08-10",
        help_text="<ul><li>Only the year is important so entering yyyy-01-01 is acceptable.</li></ul>",
        widget=forms.SelectDateWidget(years=range(1932, datetime.date.today().year),
                                      empty_label=("Choose Year", "Choose Month", "Choose Day")),
        required=True)

    class Meta:
        model = Moc
        fields = ('title', 'description', 'height', 'length',
                  'width', 'viewable_sides', 'url_photo', 'url_flickr',
                  'year_built', 'year_retired')
