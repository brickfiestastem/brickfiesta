from django.views.generic.detail import DetailView
from .models import User
from vendor.models import Business
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from .forms import AfolUserCreateForm, AfolUserChangeForm


class ProfileView(LoginRequiredMixin, DetailView):
    model = User

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['business_owner'] = False
        context['business_id'] = None
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
        return self.request.user


class SignUpView(generic.CreateView):
    form_class = AfolUserCreateForm
    template_name = 'afol/signup.html'
    success_url = '/afol/profile/'
