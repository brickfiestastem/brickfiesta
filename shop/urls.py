from django.urls import path
from . import views
app_name = 'shop'

urlpatterns = [
    path('', views.EventListView.as_view(), name='index'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('carttest/', views.CartTestView.as_view(), name='carttest'),
    path('cartcheckout/', views.CartCheckoutView.as_view(), name='cartcheckout'),
    path('details/<uuid:pk>/', views.ProductDetail.as_view(), name='details'),
    path('event/<uuid:event_id>/', views.EventProductView.as_view(), name='event'),
]
