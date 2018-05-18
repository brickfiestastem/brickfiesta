from django.urls import path
from mocs.views import CategoryListView, CategoriesListView, EventListView, EventCategoriesListView

app_name = 'mocs'

urlpatterns = [
    path('', CategoriesListView.as_view(), name='index'),
    path('events/', EventListView.as_view(), name='events'),
    path('category/<uuid:pk>/', CategoriesListView.as_view(), name='category'),
    path('eventcategories/<uuid:pk>/', EventCategoriesListView.as_view(), name='eventcategories'),
    path('details/<uuid:pk>/', MocDetails.as_view(), name='details'),
    path('edit/<uuid:pk>/', MocUpdateView.as_view(), name='edit'),
    path('add/', MocAddView.as_view(), name='add'),
]
