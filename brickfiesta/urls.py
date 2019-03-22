"""brickfiesta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import TemplateView

from event import views as main_views

urlpatterns = [
    path('', main_views.FrontPage.as_view(), name='home'),
    path('brickmaster/', admin.site.urls),
    path('about/', TemplateView.as_view(template_name='brickfiesta/about.html'), name='about'),
    path('privacy_policy/', TemplateView.as_view(template_name='brickfiesta/privacy_policy.html'),
         name='privacy_policy'),
    #    url(r'^afol/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #        auth_views.PasswordResetConfirmView,
    #        {'post_reset_redirect': '/afol/password_reset_complete'},
    #        name='password_reset_confirm'),
    path('afol/', include('afol.urls'), name='afol'),
    path('events/', include('event.urls')),
    path('games/', include('games.urls')),
    path('news/', include('news.urls')),
    path('mocs/', include('mocs.urls')),
    path('planning/', include('planning.urls')),
    path('shop/', include('shop.urls')),
    path('vendor/', include('vendor.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
]

handler404 = 'event.views.error404'
handler500 = 'event.views.error500'
