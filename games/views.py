from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, View

from .models import DoorPrizeWinner, DoorPrizePool
from event.models import Schedule
from afol.models import ScheduleAttendee, Attendee
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
        obj_scheduled_event = Schedule.objects.get(id=kwargs['schedule'])
        int_number = DoorPrizePool.objects.filter(
            schedule=obj_scheduled_event).count()
        # import ipdb; ipdb.set_trace()
        # No one is in the group so add people form the list of attendees
        if int_number == 0:
            obj_past_winners = DoorPrizeWinner.objects.filter(event=obj_scheduled_event.event).values_list('fan',
                                                                                                           flat=True)
            obj_fols = ScheduleAttendee.objects.exclude(fan__in=obj_past_winners). \
                filter(schedule=kwargs['schedule'],
                       fan__attendee__role=Attendee.ROLE_ALLACCESS,
                       )
            for fol in obj_fols:
                obj_fol, created = DoorPrizePool.objects.get_or_create(
                    schedule=fol.schedule, fan=fol.fan)
        if DoorPrizePool.objects.all().count():
            obj_winner = DoorPrizePool.objects.order_by('?').first()
            obj_entree = DoorPrizeWinner.objects.create(
                fan=obj_winner.fan, event=obj_winner.schedule.event)
            obj_winner.delete()
            return render(request, self.template_name,
                          {'number': int_number, 'winner': obj_winner, 'schedule': obj_winner.schedule})
        return render(request, self.template_name,
                      {'number': int_number, 'winner': None, 'schedule': obj_scheduled_event})
    # def post(self, request, schedule):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #     return render(request, self.template_name, {'form': form})
