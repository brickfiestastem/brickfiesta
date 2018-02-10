from django.urls import path
from . import views
app_name = 'shop'

urlpatterns = [
    path('', views.EventListView.as_view(), name='index'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('details/<uuid:product_id>/', views.Details.as_view(), name='details'),
    path('event/<uuid:event_id>/', views.EventProductView.as_view(), name='event'),
]
