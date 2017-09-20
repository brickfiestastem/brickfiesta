from django.conf.urls import include, url

import event.views

urlpatterns = [
    url(r'^locations/$', event.views.locations, name="locations"),
    url(r'^locations/(?P<location_id>[0-9a-f-]+)/$', event.views.location, name="location"),

]
    