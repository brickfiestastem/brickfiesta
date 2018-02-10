from django.urls import path, include
from .views import ProfileView, SignUpView

app_name = 'afol'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(template_name='afol/profile_detail.html'), name='profile'),
]
