from django.urls import path
from planning.views import EventListingView, ShirtSummaryView, ScheduleListView

app_name = "planning"

urlpatterns = [
    path('', EventListingView.as_view(), name='index'),
    path('shirts/<event>', ShirtSummaryView.as_view(), name='shirt'),
    path('schedule/list/<event>', ScheduleListView.as_view(), name='schedule_list'),
]
