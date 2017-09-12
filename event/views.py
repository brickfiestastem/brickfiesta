from django.views.generic import ListView
from django.shortcuts import render
from event.models import Location

class ListLocation(ListView):
    model = Location