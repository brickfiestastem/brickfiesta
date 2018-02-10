from django.views.generic.detail import DetailView
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from .forms import AfolUserCreateForm


class ProfileView(LoginRequiredMixin, DetailView):
    model = User

    def get_object(self, queryset=None):
        return self.request.user


class SignUpView(generic.CreateView):
    form_class = AfolUserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'