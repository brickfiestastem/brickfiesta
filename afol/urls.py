from django.urls import path, include, reverse_lazy

from .views import ProfileView, ProfileEditView, SignUpView, AFOLMOCsView, AFOLShirtView, AFOLShirtEditView, \
    AFOLVolunteerView, AFOLVolunteerCreateView, AFOLVolunteerListView, AFOLActivitiesCreateView, \
    AFOLActivitiesListView, AFOLActivitiesView, AFOLVoteListView, AFOLActivitiesDeleteView

app_name = 'afol'

urlpatterns = [
    path('', SignUpView.as_view(), name='signup'),

    path('activities/', AFOLActivitiesView.as_view(), name='activities'),
    path('activities/<uuid:pk>', AFOLActivitiesCreateView.as_view(),
         name='activitiescreate'),
    path('activities/delete/<uuid:pk>', AFOLActivitiesDeleteView.as_view(),
         name='activitiesdelete'),
    path('activities/list/', AFOLActivitiesListView.as_view(),
         name='activities_list'),
    path('mocs/', AFOLMOCsView.as_view(), name='mocs'),
    path('shirts/', AFOLShirtView.as_view(), name='shirts'),
    path('shirts/<uuid:pk>', AFOLShirtEditView.as_view(), name='shirtedit'),
    path('volunteer/', AFOLVolunteerView.as_view(), name='volunteer'),
    path('volunteer/<uuid:pk>', AFOLVolunteerCreateView.as_view(),
         name='volunteercreate'),
    path('volunteer/list/', AFOLVolunteerListView.as_view(),
         name='volunteer_list'),
    path('profile/', ProfileView.as_view(template_name='afol/profile_detail.html'), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='edit'),
    path('vote/', AFOLVoteListView.as_view(), name='vote_list'),
    path('', include('django.contrib.auth.urls')),
]
