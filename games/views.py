from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView

from .models import DoorPrizeWinner


@method_decorator(staff_member_required, name='dispatch')
class DoorPrizeWinnerView(ListView):
    model = DoorPrizeWinner


@method_decorator(staff_member_required, name='dispatch')
class PickDoorPrizePersonView(TemplateView):
    template_name = 'games/doorprizewinner.html'
