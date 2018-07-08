from django.urls import path

from mocs.views import CategoryListView, EventCategoriesListView, EventListView, MocAddView, \
    MocDetail, MocUpdateView, MocUpdateCategoryView, MocCreateCategoryView, MocTableTent, MocFanVote, MocPublicVote

app_name = 'mocs'

urlpatterns = [
    path('', EventListView.as_view(), name='index'),
    path('eventcategories/<uuid:event_id>/',
         EventCategoriesListView.as_view(), name='eventcategories'),
    path('category/<uuid:event_id>/<uuid:category_id>/',
         CategoryListView.as_view(), name='category'),
    path('details/<uuid:pk>/', MocDetail.as_view(), name='details'),
    path('details/vote/<uuid:moc>/<uuid:eventcategory>/', MocFanVote.as_view(), name='vote'),
    path('details/vote/public/<uuid:moc>/<uuid:eventcategory>/', MocPublicVote.as_view(), name='public_vote'),
    path('edit/<uuid:pk>/', MocUpdateView.as_view(), name='edit'),
    path('edit/category/<uuid:pk>/',
         MocUpdateCategoryView.as_view(), name='edit-category'),
    path('add/', MocAddView.as_view(), name='add'),
    path('add/category/<uuid:pk>/',
         MocCreateCategoryView.as_view(), name='add-category'),
    path('tabletent/<uuid:pk>/', MocTableTent.as_view(), name='tabletent'),

]
