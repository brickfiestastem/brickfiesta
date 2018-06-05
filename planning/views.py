from django.views.generic import ListView
from django.db.models import Avg, Count, Min, Sum
from afol.models import Shirt
from event.models import Event
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


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
