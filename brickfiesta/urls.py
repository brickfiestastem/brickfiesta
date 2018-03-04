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
from django.urls import path, include
from django.views import defaults
from django.contrib import admin
from event import views as main_views
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('', main_views.FrontPage.as_view(), name='home'),
    path('brickmaster/', admin.site.urls),
    path('afol/password_reset_done', auth_views.password_reset_done, name='password_reset_done'),
    path('afol/', include('afol.urls'), name='afol'),
    path('events/', include('event.urls')),
    path('news/', include('news.urls')),
    path('mocs/', include('mocs.urls')),
    path('shop/', include('shop.urls')),
    path('vendor/', include('vendor.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
]

handler404 = 'event.views.error404'
handler500 = 'event.views.error500'
