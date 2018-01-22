from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('details/<uuid:product_id>/', views.Details.as_view(), name='details'),
]