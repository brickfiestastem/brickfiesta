from event.utils import upload_path
from django.conf import settings
import json
import urllib
import urllib.request


def check_recaptcha(request):
    # Begin reCAPTCHA validation
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


