from django.urls import path

from . import views

app_name = 'vendor'

urlpatterns = [
    path('', views.UpcomingView.as_view(), name='index'),
    path('details/<uuid:pk>/', views.BusinessDetail.as_view(), name='details'),
    path('edit/<uuid:pk>/', views.BusinessUpdateView.as_view(), name='edit'),
    path('add/', views.BusinessAddView.as_view(), name='add'),
    path('vendors/', views.VendorListView.as_view(), name='vendors'),
    path('sponsors/', views.SponsorListView.as_view(), name='sponsors'),
    path('sponsor-request/', views.SponsorRequestDetail.as_view(),
         name='sponsor-request'),
    path('vendor-request/', views.VendorRequestDetail.as_view(),
         name='vendor-request'),
]
