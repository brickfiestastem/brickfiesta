from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import ProfileView

app_name = 'afol'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/', ProfileView.as_view(template_name='afol/profile_detail.html'), name='profile'),
]
