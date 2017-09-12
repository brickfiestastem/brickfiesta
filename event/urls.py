from django.conf.urls import patterns, include, url

import event.views


urlpatterns = patterns('',
    url(r'^$', event.views.ListLocation.as_view(),
        name='list-location',),
)