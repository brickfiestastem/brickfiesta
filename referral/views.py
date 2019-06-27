# from django.shortcuts import render

from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

from .models import Referral

# Create your views here.

class ReferralIndex(View):

    def get(self, request, referral_id):
        try:
            obj_referral = Referral.objects.get(code=referral_id)
            obj_referral.count = obj_referral.count + 1
            obj_referral.save()
            return redirect(obj_referral.url)
        except ObjectDoesNotExist:
            return redirect('https://www.brickfiesta.com')
