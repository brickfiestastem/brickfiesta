import math

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView

from afol.models import Shirt, Attendee, Badge, ScheduleVolunteer
from donations.models import Donations
from event.models import Event, Schedule, Activity
from mocs.models import Moc, MocCategories, Vote, PublicVote, EventCategory
from shop.models import OrderItem, Product
from vendor.models import Sponsor, Vendor
from .models import Program, ProgramContributors, ProgramHighlightActivity
from .utils import Table


@method_decorator(staff_member_required, name='dispatch')
class RegistrationBoothSignsView(TemplateView):
    template_name = 'planning/registration_booth_signs.html'


@method_decorator(staff_member_required, name='dispatch')
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
        context['sponsor_list'] = Sponsor.objects.all().order_by('business') \
            .filter(event=self.obj_event, status='approved')
        context['schedule_list'] = Schedule.objects.filter(
            event=self.obj_event, is_public=True, is_printable=True)
        # obj_activities = set(Schedule.objects.filter(event=self.obj_event, is_public=True).values_list('activity'))
        # TODO adjust to only get activites that are scheduled for this event.
        context['activity_list'] = Activity.objects.all().order_by('title')
        context['vendor_list'] = Vendor.objects.all().order_by('business') \
            .filter(event=self.obj_event, status='approved')
        return context


@method_decorator(staff_member_required, name='dispatch')
class EventListingView(ListView):
    queryset = Event.objects.order_by('-end_date')
    template_name = 'planning/event_list.html'


@method_decorator(staff_member_required, name='dispatch')
class ShirtSummaryView(ListView):
    template_name = 'planning/shirt_list.html'

    def get_queryset(self):
        self.obj_event = Event.objects.get(id=self.kwargs['event'])
        return Shirt.objects.filter(event=self.obj_event) \
            .values('shirt_size') \
            .annotate(shirt_count=Count('shirt_size')) \
            .order_by('shirt_size')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.obj_event
        return context


@method_decorator(staff_member_required, name='dispatch')
class ShirtCheckListView(ListView):
    template_name = 'planning/shirt_check_list.html'

    def get_queryset(self):
        self.obj_event = Event.objects.get(id=self.kwargs['event'])
        return Shirt.objects.filter(event=self.obj_event).order_by('fan__first_name', 'fan__last_name')


@method_decorator(staff_member_required, name='dispatch')
class DonationsAuctionSheetsListView(ListView):
    template_name = 'planning/donations_auction_sheets.html'

    def get_queryset(self):
        obj_event = Event.objects.get(id=self.kwargs['event'])
        return Donations.objects.filter(event=obj_event).order_by('item')


@method_decorator(staff_member_required, name='dispatch')
class BadgeCheckListView(ListView):
    template_name = 'planning/badge_check_list.html'

    def get_queryset(self):
        self.obj_event = Event.objects.get(id=self.kwargs['event'])
        return Badge.objects.filter(event=self.obj_event).order_by('fan__first_name', 'fan__last_name')


@method_decorator(staff_member_required, name='dispatch')
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


@method_decorator(staff_member_required, name='dispatch')
class ScheduleActivitiesPrintListView(ListView):
    template_name = 'planning/schedule_activities_print.html'

    def get_queryset(self):
        self.obj_event = Event.objects.get(id=self.kwargs['event'])
        return Schedule.objects.filter(event=self.obj_event, is_public=True, is_printable=True)\
            .order_by('date', 'start_time')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.obj_event
        context['printing'] = True
        return context


@method_decorator(staff_member_required, name='dispatch')
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


@method_decorator(staff_member_required, name='dispatch')
class MOCTablesView(ListView):
    model = Moc
    template_name = 'planning/moc_tables.html'

    def get_queryset(self):
        obj_event = Event.objects.get(id=self.kwargs['event'])
        obj_moc_categories = MocCategories.objects.filter(category__event=obj_event).order_by(
            'category', 'moc__width', 'moc__length')
        return obj_moc_categories

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.themes = dict()
        self.tables = list()
        self.int_current_table = 0
        self.total_number_of_tables = 0
        for obj_moc_categories in self.object_list:
            if obj_moc_categories.category not in self.themes:
                self.total_number_of_tables += 1
                int_new_table_width = math.ceil(
                    obj_moc_categories.moc.width / 30)
                int_new_table_length = math.ceil(
                    obj_moc_categories.moc.length / 60)
                obj_table = Table()
                obj_table.width = int_new_table_width * 30
                obj_table.length = int_new_table_length * 60
                obj_table.number = self.total_number_of_tables + 1
                self.tables.append(obj_table)
                self.themes[obj_moc_categories.category] = list()
                self.themes[obj_moc_categories.category].append(
                    self.total_number_of_tables)
            else:
                self.int_current_table = self.themes[obj_moc_categories.category].count(
                ) - 1

        context['tables'] = self.tables
        return context


@method_decorator(staff_member_required, name='dispatch')
class MOCListView(ListView):
    model = Moc
    template_name = 'planning/moc_list.html'

    def get_queryset(self):
        obj_event = Event.objects.get(id=self.kwargs['event'])
        obj_moc_categories = MocCategories.objects.filter(category__event=obj_event).order_by(
            'category', 'moc__width', 'moc__length')
        return obj_moc_categories


@method_decorator(staff_member_required, name='dispatch')
class MOCFullListView(ListView):
    model = Moc
    template_name = 'planning/moc_full_list.html'

    def get_queryset(self):
        obj_mocs = Moc.objects.all().annotate(category_count=Count(
            'moccategories')).order_by('category_count', 'created')
        return obj_mocs


@method_decorator(staff_member_required, name='dispatch')
class MOCTableTentView(ListView):
    model = Moc
    template_name = 'planning/moc_table_tents.html'

    def get_queryset(self):
        obj_event = Event.objects.get(id=self.kwargs['event'])
        obj_moc_categories = MocCategories.objects.filter(category__event=obj_event).order_by(
            'moc__creator__first_name', 'moc__creator__last_name')
        return obj_moc_categories


@method_decorator(staff_member_required, name='dispatch')
class AFOLBagCheckListView(ListView):
    model = OrderItem
    template_name = 'planning/afol_orderitem_list.html'

    def get_queryset(self):
        obj_event = Event.objects.get(id=self.kwargs['event'])
        return OrderItem.objects.filter(product__event=obj_event,
                                        product__product_type__in=[Product.SPONSORSHIP,
                                                                   Product.VENDOR,
                                                                   Product.CONVENTION, ]
                                        ).order_by('user__first_name', 'user__last_name',
                                                   'user__email', 'product__product_type').select_related()


@method_decorator(staff_member_required, name='dispatch')
class AFOLBarCodeView(ListView):
    model = Attendee
    template_name = 'planning/afol_barcode_8160.html'

    def get_queryset(self):
        obj_event = Event.objects.get(id=self.kwargs['event'])
        obj_attendee = Attendee.objects.filter(event=obj_event, role=self.kwargs['role'],
                                               ).order_by('fan__first_name', 'fan__last_name')
        return obj_attendee


@method_decorator(staff_member_required, name='dispatch')
class ExhibitionWillCallView(ListView):
    model = OrderItem
    template_name = 'planning/will_call_list.html'

    def get_queryset(self):
        self.obj_event = Event.objects.get(id=self.kwargs['event'])
        return OrderItem.objects.filter(product__event=self.obj_event,
                                        product__product_type__in=[
                                            Product.EXHIBITION]
                                        ).order_by('first_name', 'last_name', 'user__email', 'product__product_type')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Public Exhibition'
        context['check_item'] = 'Issued Wristband/Stamp'
        context['count'] = self.get_queryset().count()
        return context


@method_decorator(staff_member_required, name='dispatch')
class AFOLWillCallView(ListView):
    model = OrderItem
    template_name = 'planning/will_call_list.html'

    def get_queryset(self):
        self.obj_event = Event.objects.get(id=self.kwargs['event'])
        return OrderItem.objects.filter(product__event=self.obj_event,
                                        product__product_type__in=[Product.SPONSORSHIP,
                                                                   Product.VENDOR,
                                                                   Product.CONVENTION, ]
                                        ).order_by('user__last_name', 'user__first_name', 'user__email',
                                                   'product__product_type')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Fan Of LEGO'
        context['check_item'] = 'Goodie Bag'
        context['count'] = self.get_queryset().count()
        return context


@method_decorator(staff_member_required, name='dispatch')
class VendorTableTentView(ListView):
    model = Vendor
    template_name = 'planning/business_table_tents.html'

    def get_queryset(self):
        self.obj_event = Event.objects.get(id=self.kwargs['event'])
        return Vendor.objects.all().order_by('business').filter(event=self.obj_event, status='approved')


@method_decorator(staff_member_required, name='dispatch')
class SponsorTableTentView(ListView):
    model = Sponsor
    template_name = 'planning/business_table_tents.html'

    def get_queryset(self):
        self.obj_event = Event.objects.get(id=self.kwargs['event'])
        return Sponsor.objects.all().order_by('business').filter(event=self.obj_event, status='approved')


@method_decorator(staff_member_required, name='dispatch')
class AFOLCSVView(ListView):
    model = Attendee
    template_name = 'planning/afol_csv.html'

    def get_queryset(self):
        obj_event = Event.objects.get(id=self.kwargs['event'])
        obj_attendee = Attendee.objects.filter(event=obj_event,
                                               ).order_by('fan__first_name', 'fan__last_name')
        return obj_attendee


@method_decorator(staff_member_required, name='dispatch')
class VoteCounts(ListView):
    model = Vote
    template_name = 'planning/fan_vote_count.html'

    def get_queryset(self):
        obj_votes = Vote.objects.filter(category=self.kwargs['eventcategory']) \
            .values('moc').annotate(moc_count=Count('moc')).order_by('-moc_count')
        return obj_votes


@method_decorator(staff_member_required, name='dispatch')
class VoteCategories(ListView):
    model = EventCategory
    template_name = 'planning/fan_vote_eventcategory.html'

    def get_queryset(self):
        return EventCategory.objects.filter(event=self.kwargs['event'])


@method_decorator(staff_member_required, name='dispatch')
class PublicVoteCounts(ListView):
    model = PublicVote
    template_name = 'planning/public_vote_count.html'

    def get_queryset(self):
        return PublicVote.objects.filter(category__event=self.kwargs['event']) \
            .values('moc').annotate(moc_count=Count('moc')).order_by('-moc_count')


@method_decorator(staff_member_required, name='dispatch')
class VolunteerList(ListView):
    model = ScheduleVolunteer
    template_name = 'planning/schedulevolunteer_list.html'

    def get_queryset(self):
        return ScheduleVolunteer.objects.filter(schedule__event=self.kwargs['event'])\
            .order_by('fan__last_name', 'fan__first_name', 'schedule__start_time')
