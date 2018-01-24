import os
import uuid
from django.conf import settings


def upload_path_product(instance, filename):
    return upload_path('products/', filename, instance.id)


def upload_path_event(instance, filename):
    return upload_path('events/', filename, instance.id)


def upload_path(dir_name, filename, record_uuid):
    file_name, file_extension = os.path.splitext(filename)
    file_name = str(record_uuid)
    name = os.path.join(settings.MEDIA_ROOT, dir_name,
                        file_name + file_extension.lower())

    while os.path.exists(name):
        os.remove(name)

    return os.path.join(dir_name, file_name + file_extension.lower())