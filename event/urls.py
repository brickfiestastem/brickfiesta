from django.urls import path
from django.views.generic.dates import ArchiveIndexView
from .models import Event, Location
from . import views

app_name = 'event'

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('listing/', ArchiveIndexView.as_view(model=Event,
                                              date_field='end_date', allow_future=True), name='index'),
    path('details/<uuid:event_id>/', views.details, name='details'),
    path('locations/', ArchiveIndexView.as_view(model=Location,
                                                date_field='created', allow_future=True), name="locations"),
    path('location/<uuid:location_id>/', views.location, name="location"),
]
