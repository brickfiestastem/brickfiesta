from django.conf.urls import include, url

import news.views

urlpatterns = [
    url(r'^$', news.views.index, name="index"),
]
