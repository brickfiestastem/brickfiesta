from django.urls import path

from .views import DoorPrizeWinnerView
from django.views.generic import TemplateView

app_name = 'games'

urlpatterns = [
    path('', TemplateView.as_view(template_name='games/game_index.html'), name='index'),
    path('doorprizes/', TemplateView.as_view(template_name='games/game_index.html'), name='doorprize'),
    path('doorprizes/<schedule>', TemplateView.as_view(template_name='games/game_index.html'),
         name="doorprize_schedule"),
    path('doorprizes/winners/', DoorPrizeWinnerView.as_view(), name="doorprize_winners"),
]
