from django.urls import path, include
from .views import ProfileView, ProfileEditView, SignUpView, AFOLMOCsView, AFOLShirtView, AFOLShirtEditView

app_name = 'afol'

urlpatterns = [
    path('', SignUpView.as_view(), name='signup'),
    path('shirts/', AFOLShirtView.as_view(), name='shirts'),
    path('shirts/<uuid:pk>', AFOLShirtEditView.as_view(), name='shirtedit'),
    path('mocs/', AFOLMOCsView.as_view(), name='mocs'),
    path('profile/', ProfileView.as_view(template_name='afol/profile_detail.html'), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='edit'),
    path('', include('django.contrib.auth.urls')),
]
