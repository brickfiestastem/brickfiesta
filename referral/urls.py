from django.urls import path
from .views import ReferralIndex

app_name = 'referral'

urlpatterns = [
    path('<uuid:referral_id>/',
         ReferralIndex.as_view(), name='referral'),

]
