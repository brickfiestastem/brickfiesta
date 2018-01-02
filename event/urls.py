from django.conf.urls import include, url

import event.views

app_name = 'event'

urlpatterns = [
    url(r'^listing/$', event.views.index, name='index'),
    url(r'^details/(?P<event_id>[0-9a-f-]+)/$',
        event.views.details, name="details"),
    url(r'^locations/$', event.views.locations, name="locations"),
    url(r'^locations/(?P<location_id>[0-9a-f-]+)/$',
        event.views.location, name="location"),
    url(r'', event.views.frontpage, name='frontpage'),
]
