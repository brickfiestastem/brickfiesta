from django.urls import path
from . import views
app_name = 'vendor'

urlpatterns = [
    path('', views.VendorListView.as_view(), name='index'),
    path('details/<uuid:pk>/', views.BusinessDetail.as_view(), name='details'),
    path('edit/<uuid:pk>/', views.BusinessUpdateView.as_view(), name='edit'),
    path('add/', views.BusinessAddView.as_view(), name='add'),
    # path('sponsor_request/', , name='sponsor_request'),
    # path('vendor_request/', , name='vendor_request'),
]
