from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Profile, User
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile

    def get_object(self, queryset=None):
        return self.request.user
