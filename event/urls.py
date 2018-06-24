from django.urls import path
from django.views.generic.dates import ArchiveIndexView

from . import views
from .models import Event, Location
from .views import EventDetail, LocationDetail, ActivityDetail

app_name = 'event'

urlpatterns = [
    path('', views.FrontPage.as_view(), name='frontpage'),
    path('contactus/', views.ContactView.as_view(), name='contactus'),
    path('listing/', ArchiveIndexView.as_view(model=Event,
                                              date_field='end_date',
                                              allow_future=True), name='index'),
    path('details/<uuid:pk>/', EventDetail.as_view(), name='details'),
    path('activity/<uuid:pk>/', ActivityDetail.as_view(), name='activity'),
    path('locations/', ArchiveIndexView.as_view(model=Location,
                                                date_field='created',
                                                allow_future=True), name="locations"),
    path('location/<uuid:pk>/', LocationDetail.as_view(), name="location"),
]
