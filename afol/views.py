from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Profile
from vendor.models import Business
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import AfolUserCreateForm, AfolUserChangeForm


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
