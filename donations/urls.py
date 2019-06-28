from django.urls import path

from .views import DonationsListView

app_name = 'donations'

urlpatterns = [
    path('', DonationsListView.as_view(), name='index'),

]
