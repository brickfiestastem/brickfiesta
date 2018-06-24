import json
import urllib
import urllib.request

from django.conf import settings
from django.contrib import messages

from afol.models import Attendee, Badge, Fan, Shirt
from event.utils import upload_path


def check_recaptcha(request):
    # Begin reCAPTCHA validation
    host = request.get_host()
    if 'localhost' in host:
        return True
    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    return result['success']


def upload_path_product(instance, filename):
    return upload_path('products/', filename, instance.id)


def add_attendee_fan_badge_shirt(request, obj_item):
    obj_fan, is_created = Fan.objects.get_or_create(user=obj_item.user,
                                                    first_name=obj_item.first_name,
                                                    last_name=obj_item.last_name)
    if is_created:
        obj_fan.save()

    if obj_item.product.has_tshirt:
        obj_shirt, is_created = Shirt.objects.get_or_create(event=obj_item.product.event,
                                                            fan=obj_fan)
        if is_created:
            messages.info(request, "Added shirt for {}.".format(str(obj_fan)))
            obj_shirt.save()

    if obj_item.product.has_badge:
        obj_badge, is_created = Badge.objects.get_or_create(event=obj_item.product.event,
                                                            fan=obj_fan,
                                                            badge_name="{} {}".format(obj_fan.first_name,
                                                                                      obj_fan.last_name))
        if is_created:
            messages.info(request, "Added badge for {}.".format(str(obj_fan)))
            obj_badge.save()

    if obj_item.product.product_type == 'vendor':
        obj_attendee, is_created = Attendee.objects.get_or_create(event=obj_item.product.event,
                                                                  fan=obj_fan,
                                                                  role=Attendee.ROLE_VENDOR)
        if is_created:
            messages.info(
                request, "Added attendee vendor for {}.".format(str(obj_fan)))
            obj_attendee.save()
    if obj_item.product.product_type == 'sponsor':
        obj_attendee, is_created = Attendee.objects.get_or_create(event=obj_item.product.event,
                                                                  fan=obj_fan,
                                                                  role=Attendee.ROLE_SPONSOR)
        if is_created:
            messages.info(
                request, "Added attendee sponsor for {}.".format(str(obj_fan)))
            obj_attendee.save()
    if obj_item.product.product_type == 'convention':
        str_role = Attendee.ROLE_ATTENDEE
        if "companion" in obj_item.product.title.lower():
            str_role = Attendee.ROLE_COMPANION
        if "all" in obj_item.product.title.lower() and "access" in obj_item.product.title.lower():
            str_role = Attendee.ROLE_ALLACCESS

        obj_attendee, is_created = Attendee.objects.get_or_create(event=obj_item.product.event,
                                                                  fan=obj_fan,
                                                                  role=str_role)
        if is_created:
            messages.info(request, "Added attendee {} for {}.".format(
                str_role, str(obj_fan)))
            obj_attendee.save()
