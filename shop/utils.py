from event.utils import upload_path


def upload_path_product(instance, filename):
    return upload_path('products/', filename, instance.id)
