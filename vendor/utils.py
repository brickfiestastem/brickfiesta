from event.utils import upload_path


def upload_path_vendor(instance, filename):
    return upload_path('vendor/', filename, instance.id)
