from event.utils import upload_path


def upload_path_mocs(instance, filename):
    return upload_path('mocs/', filename, instance.id)
