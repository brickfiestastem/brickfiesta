from django.urls import path, include
from .views import ProfileView, ProfileEditView, SignUpView, AFOLMOCsView

app_name = 'afol'

urlpatterns = [
    path('', SignUpView.as_view(), name='signup'),
    path('mocs/', AFOLMOCsView.as_view(), name='mocs'),
    path('profile/', ProfileView.as_view(template_name='afol/profile_detail.html'), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='edit'),
    path('', include('django.contrib.auth.urls')),
]
