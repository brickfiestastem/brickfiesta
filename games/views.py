from random import shuffle
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
        obj_pool = DoorPrizePool.objects.filter(schedule=obj_scheduled_event)
        int_number = obj_pool.count()
        # import ipdb; ipdb.set_trace()
        # No one is in the group so add people form the list of attendees
        if int_number == 0:
            obj_past_winners = DoorPrizeWinner.objects.filter(event=obj_scheduled_event.event).values_list('fan',
                                                                                                           flat=True)
            obj_fols = list(ScheduleAttendee.objects.exclude(fan__in=obj_past_winners). \
                filter(schedule=obj_scheduled_event,
                       fan__attendee__role=Attendee.ROLE_ALLACCESS,
                       ))

            if len(obj_fols) == 0:
                return render(request, self.template_name,
                              {'number': int_number,
                               'winner': None,
                               'message': 'No people left to draw from according to who is registered for this ' \
                               'scheduled activity and the door prize winner list for this event!',
                               'schedule': obj_scheduled_event})

            shuffle(obj_fols)

            for fol in obj_fols:
                obj_fol, created = DoorPrizePool.objects.get_or_create(
                    schedule=fol.schedule, fan=fol.fan)
            return render(request, self.template_name,
                          {'number': int_number,
                           'winner': None,
                           'message': 'Just built a list of potential door prize FOLs, refresh to start drawing names.',
                           'schedule': obj_scheduled_event})
        else:
            obj_winner = obj_pool.first()
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
