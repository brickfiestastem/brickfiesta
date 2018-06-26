from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from afol.models import Shirt
from event.models import Event, Schedule


@method_decorator(login_required, name='dispatch')
class EventListingView(ListView):
    queryset = Event.objects.order_by('-end_date')
    template_name = 'planning/event_list.html'


@method_decorator(login_required, name='dispatch')
class ShirtSummaryView(ListView):
    template_name = 'planning/shirt_list.html'

    def get_queryset(self):
        self.obj_event = Event.objects.get(id=self.kwargs['event'])
        return Shirt.objects.filter(event=self.obj_event).values('shirt_size').annotate(shirt_count=Count('shirt_size'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.obj_event
        return context


@method_decorator(login_required, name='dispatch')
class ScheduleListView(ListView):
    template_name = 'planning/schedule_list.html'

    def get_queryset(self):
        self.obj_event = Event.objects.get(id=self.kwargs['event'])
        return Schedule.objects.filter(event=self.obj_event).annotate(
            volunteer_count=Count('schedulevolunteer'),
            attendee_count=Count('scheduleattendee'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.obj_event
        return context


@method_decorator(login_required, name='dispatch')
class SchedulePrintListView(ListView):
    template_name = 'planning/schedule_print.html'

    def get_queryset(self):
        self.obj_event = Event.objects.get(id=self.kwargs['event'])
        return Schedule.objects.filter(event=self.obj_event, is_public=True, is_printable=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.obj_event
        return context
