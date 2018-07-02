import datetime

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.edit import CreateView

from event.models import Schedule
from mocs.models import Moc
from vendor.models import Business
from .forms import AfolUserCreateForm, AfolUserChangeForm, ShirtChangeForm, ScheduleVolunteerForm
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
            creator__in=Fan.objects.filter(user=request.user))
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
        return Schedule.objects.filter(event__end_date__gte=today, event__in=obj_events).annotate(
            volunteer_count=Count('schedulevolunteer'))

    def get_context_data(self, **kwargs):
        context = super(AFOLVolunteerView, self).get_context_data(**kwargs)
        context['can_volunteer'] = True
        return context

    def post(self, request):
        obj_form = ScheduleVolunteerForm(request.POST, instance=Fan.objects.get(
            fan=request.POST.get('fan'), schedule=request.POST.get('schedule')))
        if obj_form.is_valid():
            obj_form.save()
        return


@method_decorator(login_required, name='dispatch')
class AFOLVolunteerCreateView(CreateView):
    model = ScheduleVolunteer
    form_class = ScheduleVolunteerForm
    success_url = reverse_lazy('afol:volunteer')

    def dispatch(self, request, *args, **kwargs):
        self.schedule = Schedule.objects.get(pk=kwargs['pk'])
        return super(AFOLVolunteerCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AFOLVolunteerCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.schedule = self.schedule
        return super(AFOLVolunteerCreateView, self).form_valid(form)
