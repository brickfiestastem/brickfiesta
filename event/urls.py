from django.urls import path
from django.views.generic.dates import ArchiveIndexView
from .models import Event, Location
from . import views
from .views import EventDetail, LocationDetail
from django.conf.urls import handler400, handler403, handler404, handler500

app_name = 'event'

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('contactus/', views.ContactView.as_view(), name='contactus'),
    path('listing/', ArchiveIndexView.as_view(model=Event,
                                              date_field='end_date',
                                              allow_future=True), name='index'),
    path('details/<uuid:pk>/', EventDetail.as_view(), name='details'),
    path('locations/', ArchiveIndexView.as_view(model=Location,
                                                date_field='created',
                                                allow_future=True), name="locations"),
    path('location/<uuid:pk>/', LocationDetail.as_view(), name="location"),
]