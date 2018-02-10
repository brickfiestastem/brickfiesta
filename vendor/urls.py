from django.urls import path
from . import views
app_name = 'vendor'

urlpatterns = [
    path('', views.VendorListView.as_view(), name='index'),
    path('details/<uuid:pk>/', views.VendorDetail.as_view(), name='details'),
]
