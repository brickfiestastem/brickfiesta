from django import forms

from games.models import DoorPrizeWinner


class DoorPrizeWinnerForm(forms.ModelForm):
    class Meta:
        model = DoorPrizeWinner
        fields = ['fan', 'event']
