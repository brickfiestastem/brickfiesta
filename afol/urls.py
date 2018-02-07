from django.urls import path, include
from django.contrib.auth import views as auth_views

app_name = 'afol'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/', auth_views.PasswordChangeView.as_view()),
]
