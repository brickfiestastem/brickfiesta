from django.urls import path
from mocs.views import CategoryListView

app_name = 'mocs'

urlpatterns = [
    path('', CategoryListView.as_view(), name='index'),
]
