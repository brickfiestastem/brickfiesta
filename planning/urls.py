from django.urls import path

from planning.views import EventListingView, ShirtSummaryView, ScheduleListView, SchedulePrintListView, ProgramView, \
    MOCListView, MOCFullListView, MOCTablesView, MOCTableTentView, AFOLBagCheckListView, ExhibitionWillCallView, AFOLWillCallView, \
    RegistrationBoothSignsView, VendorTableTentView, SponsorTableTentView, AFOLBarCodeView, ShirtCheckListView, \
    BadgeCheckListView, ScheduleActivitiesPrintListView, AFOLCSVView, VoteCounts, PublicVoteCounts, VoteCategories, \
    VolunteerList, DonationsAuctionSheetsListView, MOCMicroCardView

app_name = "planning"

urlpatterns = [
    path('', EventListingView.as_view(), name='index'),
    path('activities/sheets/<event>',
         ScheduleActivitiesPrintListView.as_view(), name='activities_sheets'),
    path('afol/bag/<event>', AFOLBagCheckListView.as_view(), name='afol_bags'),
    path('afol/csv/<event>', AFOLCSVView.as_view(), name='afol_csv'),
    path('afol/barcodes/<event>/<str:role>',
         AFOLBarCodeView.as_view(), name='afol_barcodes'),
    path('afol/barcodes/88695/<event>/<str:role>', AFOLBarCodeView.as_view(template_name='planning/afol_barcode_88695.html'),
         name='afol_barcodes_88695'),
    path('afol/willcall/<event>', AFOLWillCallView.as_view(), name='afol_will_call'),
    path('badge/checklist/<event>',
         BadgeCheckListView.as_view(), name='badge_check_list'),
    path('donations/auction_sheets/<event>',
         DonationsAuctionSheetsListView.as_view(), name='donation_auction_sheets'),
    path('exhibition/willcall/<event>',
         ExhibitionWillCallView.as_view(), name='exhibition_will_call'),
    path('program/<event>', ProgramView.as_view(), name='program'),
    path('mocs/list/<event>', MOCListView.as_view(), name='moc_list'),
    path('mocs/fulllist/<event>', MOCFullListView.as_view(), name='moc_full_list'),
    path('mocs/tables/<event>', MOCTablesView.as_view(), name='moc_tables'),
    path('mocs/table_tents/<event>',
         MOCTableTentView.as_view(), name='moc_table_tents'),
    path('mocs/micro_table_tents/<event>',
         MOCMicroCardView.as_view(), name='moc_micro_table_tents'),
    path('registration_booth/table_tents/', RegistrationBoothSignsView.as_view(),
         name='registration_booth_table_tents'),
    path('schedule/list/<event>', ScheduleListView.as_view(), name='schedule_list'),
    path('schedule/print/<event>',
         SchedulePrintListView.as_view(), name='schedule_print'),
    path('schedule/print/scheduled/<event>',
         SchedulePrintListView.as_view(template_name='planning/schedule_activities_print.html'), name='schedule_activities_print'),
    path('schedule/print/room/<event>',
         SchedulePrintListView.as_view(
             template_name='planning/schedule_print_room.html'),
         name='schedule_print_room', ),
    path('shirts/<event>', ShirtSummaryView.as_view(), name='shirt'),
    path('shirts/checklist/<event>',
         ShirtCheckListView.as_view(), name='shirt_check_list'),
    path('sponsor/table_tents/<event>',
         SponsorTableTentView.as_view(), name='sponsor_table_tents'),
    path('vendor/table_tents/<event>',
         VendorTableTentView.as_view(), name='vendor_table_tents'),
    path('vote/fan/<event>', VoteCategories.as_view(), name='vote_fan_category'),
    path('vote/fan/category/<eventcategory>',
         VoteCounts.as_view(), name='vote_fan_count'),
    path('vote/public/<event>', PublicVoteCounts.as_view(), name='vote_public'),
    path('volunteers/<event>', VolunteerList.as_view(), name='volunteer_list')
]
