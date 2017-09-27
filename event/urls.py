from django.conf.urls import include, url

import event.views

app_name = 'event'

urlpatterns = [
    url(r'^$', event.views.index, name='index'),
    url(r'^(?P<event_id>[0-9a-f-]+)/$', event.views.details, name="event"),
    url(r'^locations/$', event.views.locations, name="locations"),
    url(r'^locations/(?P<location_id>[0-9a-f-]+)/$', event.views.location, name="location"),

]
    