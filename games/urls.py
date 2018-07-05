from django.urls import path

from .views import DoorPrizeWinnerView, PickDoorPrizePersonView, PickDoorPrizeSchedule
from django.views.generic import TemplateView

app_name = 'games'

urlpatterns = [
    path('', TemplateView.as_view(
        template_name='games/game_index.html'), name='index'),
    path('doorprizes/', PickDoorPrizeSchedule.as_view(), name='doorprize'),
    path('doorprizes/<schedule>', PickDoorPrizePersonView.as_view(),
         name="doorprize_schedule"),
    path('doorprizes/winners/', DoorPrizeWinnerView.as_view(),
         name="doorprize_winners"),
]
