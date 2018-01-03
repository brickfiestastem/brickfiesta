from django.urls import path
from . import views

app_name = 'event'

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('listing/', views.index, name='index'),
    path('details/<uuid:event_id>/', views.details, name='details'),
    path('locations/', views.locations, name="locations"),
    path('location/<uuid:location_id>/', views.location, name="location"),
]
