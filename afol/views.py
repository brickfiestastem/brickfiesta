import datetime

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import DetailView, ListView, UpdateView, FormView, CreateView

from event.models import Schedule
from mocs.models import Moc, Vote
from vendor.models import Business
from .forms import AfolUserCreateForm, AfolUserChangeForm, ShirtChangeForm, ScheduleVolunteerForm, ScheduleAttendeeForm
from .models import Attendee, Profile, Fan, Shirt, ScheduleVolunteer, ScheduleAttendee


class ProfileView(LoginRequiredMixin, DetailView):
    model = User

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['business_owner'] = False
        context['business_id'] = None
        context['profile'] = Profile.objects.filter(
            user=self.request.user).first()
        if Business.objects.filter(user=self.request.user).exists():
            context['business_owner'] = True
            context['business_id'] = Business.objects.filter(
                user=self.request.user).first().id
        return context


class ProfileEditView(LoginRequiredMixin, generic.UpdateView):
    form_class = AfolUserChangeForm
    template_name = 'afol/profile_edit.html'
    success_url = '/afol/profile/'
    model = User

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        profile = self.get_object()
        profile.birth_date = form.cleaned_data.get('birth_date')
        profile.bricklink_username = form.cleaned_data.get(
            'bricklink_username')
        profile.flickr_handle = form.cleaned_data.get('flickr_handle')
        profile.twitter_handle = form.cleaned_data.get('twitter_handle')
        profile.save()
        return redirect('afol:profile')


class SignUpView(generic.CreateView):
    model = User
    form_class = AfolUserCreateForm
    template_name = 'afol/signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.email = form.cleaned_data.get('email')
        user.save()
        user.refresh_from_db()
        # profile = Profile.objects.create(user=user)
        user.profile.birth_date = form.cleaned_data.get('birth_date')
        user.profile.bricklink_username = form.cleaned_data.get(
            'bricklink_username')
        user.profile.flickr_handle = form.cleaned_data.get('flickr_handle')
        user.profile.twitter_handle = form.cleaned_data.get('twitter_handle')
        user.save()
        login(self.request, user)
        return redirect('afol:profile')


@method_decorator(login_required, name='dispatch')
class AFOLMOCsView(ListView):
    model = Moc

    def get(self, request):
        obj_mocs = Moc.objects.filter(
            creator__in=Fan.objects.filter(user=request.user)).annotate(category_count=Count('moccategories'))
        return render(request,
                      'afol/moc_list.html', {'object_list': obj_mocs})


@method_decorator(login_required, name='dispatch')
class AFOLShirtView(ListView):
    model = Shirt
    template_name = 'afol/shirt_list.html'

    def get_context_data(self, **kwargs):
        context = super(AFOLShirtView, self).get_context_data(**kwargs)
        context['object_list'] = Shirt.objects.filter(
            fan__in=Fan.objects.filter(user=self.request.user))
        return context

    def post(self, request):
        obj_shirtform = ShirtChangeForm(request.POST, instance=Shirt.objects.get(
            fan=request.POST.get('fan'), event=request.POST.get('event')))
        if obj_shirtform.is_valid():
            obj_shirtform.save()
        obj_shirts = Shirt.objects.filter(
            fan__in=Fan.objects.filter(user=self.request.user))
        return render(request, 'afol/shirt_list.html', {'object_list': obj_shirts})


@method_decorator(login_required, name='dispatch')
class AFOLShirtEditView(UpdateView):
    model = Shirt
    form_class = ShirtChangeForm
    success_url = reverse_lazy('afol:shirts')


@method_decorator(login_required, name='dispatch')
class AFOLVolunteerView(ListView):
    model = Schedule
    template_name = 'afol/volunteer_list.html'

    def get_form_kwargs(self):
        kwargs = super(AFOLVolunteerView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        obj_events = Attendee.objects.filter(
            fan__user=self.request.user).values('event')
        today = datetime.date.today()
        return Schedule.objects.filter(event__end_date__gte=today, event__in=obj_events, is_public=True).annotate(
            volunteer_count=Count('schedulevolunteer'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AFOLVolunteerView, self).get_context_data(**kwargs)
        context['can_volunteer'] = True
        return context

    def post(self, request, *args, **kwargs):
        # TODO figure out why create view is posting to list view refactor to form_valid logic
        obj_fan = Fan.objects.get(id=request.POST['fan'])
        obj_schedule = Schedule.objects.get(id=request.POST['schedule'])
        obj_volunteer, created = ScheduleVolunteer.objects.get_or_create(
            fan=obj_fan, schedule=obj_schedule)
        obj_volunteer.save()
        return redirect('afol:volunteer_list')


@method_decorator(login_required, name='dispatch')
class AFOLVolunteerCreateView(CreateView):
    model = ScheduleVolunteer
    form_class = ScheduleVolunteerForm
    success_url = reverse_lazy('afol:volunteer')

    def get_form_kwargs(self):
        kwargs = super(AFOLVolunteerCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AFOLVolunteerCreateView,
                        self).get_context_data(**kwargs)
        context['schedule'] = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        return context

    def get_initial(self):
        self.obj_schedule = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        return {
            'schedule': self.obj_schedule,
        }

    def form_valid(self, form):
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class AFOLVolunteerListView(ListView):
    model = ScheduleVolunteer
    template_name = 'afol/volunteer_list.html'
    success_url = reverse_lazy('afol:volunteer')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AFOLVolunteerListView, self).get_context_data(**kwargs)
        obj_scheduled = ScheduleVolunteer.objects.filter(
            fan__user=self.request.user).values_list('schedule__id', flat=True)
        context['schedule_list'] = Schedule.objects.filter(
            id__in=obj_scheduled).order_by('-event')
        return context

    def get_queryset(self):
        obj_scheduled = ScheduleVolunteer.objects.filter(
            fan__user=self.request.user)
        return obj_scheduled


@method_decorator(login_required, name='dispatch')
class AFOLActivitiesView(ListView):
    model = Schedule
    template_name = 'afol/activities_list.html'

    def get_form_kwargs(self):
        kwargs = super(AFOLActivitiesView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        obj_events = Attendee.objects.filter(
            fan__user=self.request.user).values('event')
        today = datetime.date.today()
        return Schedule.objects.filter(event__end_date__gte=today, event__in=obj_events, is_public=True).annotate(
            attendee_count=Count('scheduleattendee'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AFOLActivitiesView, self).get_context_data(**kwargs)
        context['can_attend'] = True
        return context

    def post(self, request, *args, **kwargs):
        # TODO figure out why create view is posting to list view refactor to form_valid logic
        obj_fan = Fan.objects.get(id=request.POST['fan'])
        obj_schedule = Schedule.objects.get(id=request.POST['schedule'])
        obj_volunteer, created = ScheduleAttendee.objects.get_or_create(
            fan=obj_fan, schedule=obj_schedule)
        obj_volunteer.save()
        return redirect('afol:activities_list')


@method_decorator(login_required, name='dispatch')
class AFOLActivitiesCreateView(CreateView):
    model = ScheduleAttendee
    form_class = ScheduleAttendeeForm
    success_url = reverse_lazy('afol:activities')

    def get_form_kwargs(self):
        kwargs = super(AFOLActivitiesCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AFOLActivitiesCreateView,
                        self).get_context_data(**kwargs)
        context['schedule'] = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        return context

    def get_initial(self):
        self.obj_schedule = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        return {
            'schedule': self.obj_schedule,
        }

    def form_valid(self, form):
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class AFOLActivitiesListView(ListView):
    model = ScheduleAttendee
    template_name = 'afol/activities_list.html'
    success_url = reverse_lazy('afol:activities')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AFOLActivitiesListView,
                        self).get_context_data(**kwargs)
        obj_scheduled = ScheduleAttendee.objects.filter(
            fan__user=self.request.user).values_list('schedule__id', flat=True)
        context['schedule_list'] = Schedule.objects.filter(
            id__in=obj_scheduled).order_by('-event')
        return context

    def get_queryset(self):
        obj_scheduled = ScheduleAttendee.objects.filter(
            fan__user=self.request.user)
        return obj_scheduled


class AFOLVoteListView(ListView):
    model = Vote
    template_name = 'afol/vote_list.html'

    def get_queryset(self):
        obj_fan = Fan.objects.filter(user=self.request.user)
        return Vote.objects.filter(fan__in=obj_fan)
