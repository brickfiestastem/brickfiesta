from event.utils import upload_path


def upload_path_barcodes(instance, filename):
    return upload_path('barcodes/', filename, instance.id)