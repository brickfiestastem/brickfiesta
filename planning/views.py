import math

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView

from afol.models import Shirt
from event.models import Event, Schedule, Activity
from mocs.models import Moc, MocCategories
from vendor.models import Sponsor, Vendor
from shop.models import OrderItem, Product
from .models import Program, ProgramContributors, ProgramHighlightActivity


class RegistrationBoothSignsView(TemplateView):
    template_name = 'planning/registration_booth_signs.html'


class ProgramView(TemplateView):
    template_name = 'planning/program_print.html'

    def get_queryset(self):
        return Event.objects.get(id=self.kwargs['event'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.obj_event = Event.objects.get(id=self.kwargs['event'])
        context['printing'] = True
        context['event'] = self.obj_event
        context['program'] = Program.objects.get(event=self.obj_event)
        context['program_contributors'] = ProgramContributors.objects.filter(
            program=context['program']).order_by('order')
        context['program_highlights'] = ProgramHighlightActivity.objects.filter(
            program=context['program'])
        context['sponsor_list'] = Sponsor.objects.all().order_by('business')\
            .filter(event=self.obj_event, status='approved')
        context['schedule_list'] = Schedule.objects.filter(
            event=self.obj_event, is_public=True, is_printable=True)
        # obj_activities = set(Schedule.objects.filter(event=self.obj_event, is_public=True).values_list('activity'))
        # TODO adjust to only get activites that are scheduled for this event.
        context['activity_list'] = Activity.objects.all().order_by('title')
        context['vendor_list'] = Vendor.objects.all().order_by('business')\
            .filter(event=self.obj_event, status='approved')
        return context


@method_decorator(login_required, name='dispatch')
class EventListingView(ListView):
    queryset = Event.objects.order_by('-end_date')
    template_name = 'planning/event_list.html'


@method_decorator(login_required, name='dispatch')
class ShirtSummaryView(ListView):
    template_name = 'planning/shirt_list.html'

    def get_queryset(self):
        self.obj_event = Event.objects.get(id=self.kwargs['event'])
        return Shirt.objects.filter(event=self.obj_event)\
                            .values('shirt_size')\
                            .annotate(shirt_count=Count('shirt_size'))\
                            .order_by('shirt_size')

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
        context['printing'] = True
        return context


@method_decorator(login_required, name='dispatch')
class MOCTablesView(ListView):
    model = Moc
    template_name = 'planning/moc_tables.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.tables = list()
        self.table_length = 72
        self.table_width = 30
        for obj_moc in self.object_list:
            int_new_table_width = math.ceil(obj_moc.width / 30)
            int_new_table_length = math.ceil(obj_moc.length / 72)

        context['tables'] = self.tables
        return context


@method_decorator(login_required, name='dispatch')
class MOCTableTentView(ListView):
    model = Moc
    template_name = 'planning/moc_table_tents.html'

    def get_queryset(self):
        obj_event = Event.objects.get(id=self.kwargs['event'])
        obj_moc_categories = MocCategories.objects.filter(category__event=obj_event).order_by(
            'moc__creator__first_name', 'moc__creator__last_name')
        return obj_moc_categories

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class AFOLBagCheckListView(ListView):
    model = OrderItem
    template_name = 'planning/afol_orderitem_list.html'

    def get_queryset(self):
        obj_event = Event.objects.get(id=self.kwargs['event'])
        return OrderItem.objects.filter(product__event=obj_event,
                                        product__product_type__in=[Product.SPONSORSHIP,
                                                                   Product.VENDOR,
                                                                   Product.CONVENTION, ]
                                        ).order_by('user__first_name', 'user__last_name', 'user__email')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class ExhibitionWillCallView(ListView):
    model = OrderItem
    template_name = 'planning/will_call_list.html'

    def get_queryset(self):
        self.obj_event = Event.objects.get(id=self.kwargs['event'])
        return OrderItem.objects.filter(product__event=self.obj_event,
                                        product__product_type__in=[
                                            Product.EXHIBITION]
                                        ).order_by('first_name', 'last_name', 'user__email')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Public Exhibition'
        context['check_item'] = 'Issued Wristband/Stamp'
        context['count'] = self.get_queryset().count()
        return context


@method_decorator(login_required, name='dispatch')
class AFOLWillCallView(ListView):
    model = OrderItem
    template_name = 'planning/will_call_list.html'

    def get_queryset(self):
        self.obj_event = Event.objects.get(id=self.kwargs['event'])
        return OrderItem.objects.filter(product__event=self.obj_event,
                                        product__product_type__in=[Product.SPONSORSHIP,
                                                                   Product.VENDOR,
                                                                   Product.CONVENTION, ]
                                        ).order_by('user__last_name', 'user__first_name', 'user__email')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Fan Of LEGO'
        context['check_item'] = 'Goodie Bag'
        context['count'] = self.get_queryset().count()
        return context


class VendorTableTentView(ListView):
    model = Vendor
    template_name = 'planning/business_table_tents.html'

    def get_queryset(self):
        self.obj_event = Event.objects.get(id=self.kwargs['event'])
        return Vendor.objects.all().order_by('business').filter(event=self.obj_event, status='approved')


class SponsorTableTentView(ListView):
    model = Sponsor
    template_name = 'planning/business_table_tents.html'

    def get_queryset(self):
        self.obj_event = Event.objects.get(id=self.kwargs['event'])
        return Sponsor.objects.all().order_by('business').filter(event=self.obj_event, status='approved')
