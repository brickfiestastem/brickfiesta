from django.urls import path

from planning.views import EventListingView, ShirtSummaryView, ScheduleListView, SchedulePrintListView, ProgramView, \
    MOCTablesView

app_name = "planning"

urlpatterns = [
    path('', EventListingView.as_view(), name='index'),
    path('program/<event>', ProgramView.as_view(), name='program'),
    path('mocs/tables/', MOCTablesView.as_view(), name='moc_tables'),
    path('schedule/list/<event>', ScheduleListView.as_view(), name='schedule_list'),
    path('schedule/print/<event>',
         SchedulePrintListView.as_view(), name='schedule_print'),
    path('shirts/<event>', ShirtSummaryView.as_view(), name='shirt'),

]
