import datetime
from datetime import timedelta

from django.conf import settings
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormView

from afol.models import Fan, ScheduleVolunteer, ScheduleAttendee
from event.models import Announcement, Event, Location, Schedule, Activity
from shop.utils import check_recaptcha
from vendor.models import Sponsor, Vendor
from .forms import ContactForm


class FrontPage(TemplateView):
    template_name = 'event/frontpage.html'

    def get_context_data(self, **kwargs):
        today = datetime.date.today()
        yesterday = datetime.date.today() - timedelta(days=1)
        context = super().get_context_data(**kwargs)
        context['announcements'] = Announcement.objects.filter(
            end_date__gte=today)
        obj_events_current = Event.objects.all().order_by(
            '-start_date').filter(start_date__lte=today, end_date__gte=today)
        context['events_current'] = obj_events_current
        obj_events_upcoming = Event.objects.all().order_by(
            'start_date').filter(start_date__gt=today)
        context['events_upcoming'] = obj_events_upcoming
        context['events_past'] = Event.objects.all().order_by(
            '-start_date').filter(end_date__lt=today)
        context['sponsor_list'] = Sponsor.objects.all().order_by(
            'business').filter(event__in=obj_events_upcoming | obj_events_current, status='approved')
        context['vendor_list'] = Vendor.objects.all().order_by(
            'business').filter(event__in=obj_events_upcoming | obj_events_current, status='approved')
        return context


class ContactView(FormView):
    template_name = 'event/contactus.html'
    form_class = ContactForm
    success_url = '/events/'

    def form_valid(self, form):
        if not check_recaptcha(self.request):
            form.add_error(
                None, 'You failed the human test. Try the reCAPTCHA again.')
        else:
            form.send_email()
        return super().form_valid(form)


class ActivityDetail(DetailView):
    model = Activity

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schedule_list'] = None
        if self.request.user.is_authenticated:
            context['schedule_list'] = Schedule.objects.filter(
                activity=self.object, is_public=True).annotate(
                volunteer_count=Count('schedulevolunteer'),
                attendee_count=Count('scheduleattendee'))
        else:
            context['schedule_list'] = Schedule.objects.filter(
                activity=self.object, is_public=True)
        return context


class ScheduledActivityView(DetailView):
    model = Schedule

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schedule_list'] = Schedule.objects.filter(
            activity=self.object.activity, event=self.object.event, is_public=True)
        if self.request.user.is_authenticated:
            context['schedule_list'] = Schedule.objects.filter(
                activity=self.object.activity, event=self.object.event, is_public=True).annotate(
                volunteer_count=Count('schedulevolunteer'),
                attendee_count=Count('scheduleattendee'))
            context['can_volunteer'] = True
            obj_fan = Fan.objects.filter(user=self.request.user)
            context['is_volunteer'] = ScheduleVolunteer.objects.filter(
                schedule=self.object, fan__in=obj_fan).count()
            context['attendees'] = ScheduleAttendee.objects.filter(
                schedule=self.object).order_by('created')
        return context


class EventDetail(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        today = datetime.date.today()
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the sponsors and vendors
        context['announcements'] = Announcement.objects.filter(
            event=self.object, end_date__gte=today)
        context['sponsor_list'] = Sponsor.objects.filter(
            event=self.object, status='approved')
        context['vendor_list'] = Vendor.objects.filter(
            event=self.object, status='approved')
        context['schedule_list'] = Schedule.objects.filter(
            event=self.object, is_public=True)
        return context


class LocationDetail(DetailView):
    model = Location

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the sponsors and vendors
        context['event_list'] = Event.objects.filter(location=self.object)

        context['map_search'] = "{}, {}, {}, {}".format(self.object.street,
                                                        self.object.locality,
                                                        self.object.region,
                                                        self.object.country)
        context['google_map_key'] = settings.GOOGLE_MAP_KEY
        return context


def handle_error(request, template='brickfiesta/404.html', status_code=404):
    return render(request, template_name=template, status=status_code)


def error404(request):
    return handle_error(request)


def error500(request):
    return handle_error(request, 'brickfiesta/500.html', 500)
