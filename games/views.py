from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, View

from .models import DoorPrizeWinner, DoorPrizePool
from event.models import Schedule
from afol.models import ScheduleAttendee
from .forms import DoorPrizeWinnerForm


@method_decorator(staff_member_required, name='dispatch')
class DoorPrizeWinnerView(ListView):
    model = DoorPrizeWinner

@method_decorator(staff_member_required, name='dispatch')
class PickDoorPrizeSchedule(ListView):
    template_name = 'games/doorprize_schedule_list.html'
    model = Schedule

@method_decorator(staff_member_required, name='dispatch')
class PickDoorPrizePersonView(View):
    model = DoorPrizeWinner
    form_class = DoorPrizeWinnerForm
    template_name = 'games/doorprizewinner.html'

    def get(self, request, *args, **kwargs):
        int_number = DoorPrizePool.objects.filter(schedule=kwargs['schedule']).count()
        if int_number == 0:
            obj_fols = ScheduleAttendee.objects.filter(schedule=kwargs['schedule'])
            for fol in obj_fols:
                obj_fol, created = DoorPrizePool.objects.get_or_create(schedule=fol.schedule, fan=fol.fan)
        obj_winner = DoorPrizePool.objects.order_by('?').first()
        obj_entree, created = DoorPrizeWinner.objects.get_or_create(fan=obj_winner.fan, event=obj_winner.schedule.event)
        obj_winner.delete()
        # print(obj_winner)
        #
        # form = DoorPrizeWinnerForm()
        # fan = obj_winner.fan
        # event = obj_winner.schedule.event
        return render(request, self.template_name, {'number': int_number, 'winner': obj_winner, 'schedule': obj_winner.schedule})

    # def post(self, request, schedule):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #     return render(request, self.template_name, {'form': form})


