from django.conf.urls import include, url

import news.views

app_name = 'news'

urlpatterns = [
    url(r'^$', news.views.index, name="index"),
]
