from django.conf.urls import include, url

import mocs.views

app_name = 'mocs'

urlpatterns = [
    url(r'^$', mocs.views.index, name="index"),
    url(r'^add/$', mocs.views.add, name="add"),
    url(r'^(?P<moc_id>[0-9a-f-]+)/$', mocs.views.details, name="details"),
    url(r'^edit/(?P<moc_id>[0-9a-f-]+)/$', mocs.views.edit, name="edit"),
    url(r'^category/(?P<category_id>[0-9a-f-]+)/$',
        mocs.views.category, name="category"),
    url(r'^categories/$', mocs.views.categories, name="categories"),
]
