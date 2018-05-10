from django.core.management.base import BaseCommand
from planning.utils import image_square


class Command(BaseCommand):
    help = 'Converts a rectange image into a transparent square image.'

    def add_arguments(self, parser):
        parser.add_argument('image_path', nargs='+', type=str)

    def handle(self, *args, **options):
        for image_path in options['image_path']:
            new_square = image_square(image_path)
            new_square.save(image_path)

