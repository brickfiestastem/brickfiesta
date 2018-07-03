import math
import subprocess

import barcode
from PIL import Image, ImageDraw, ImageFont
from barcode.writer import ImageWriter
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Converts a rectange image into a transparent square image.'

    def add_arguments(self, parser):
        parser.add_argument('id', nargs='?')
        parser.add_argument('center_text', nargs='?')
        parser.add_argument('print_size', nargs='?')
        parser.add_argument('--print', action='store_true', dest='print', default=False)

    def handle(self, *args, **options):
        self.int_label_width = 991
        self.int_label_height = 306
        self.int_label_length = '29x90'
        if options['print_size'] == 62:
            self.int_label_width = 1109
            self.int_label_height = 696
            self.int_label_length = '62'
        self.printer = "/dev/usb/lp3"
        self.tmp_image = "./tmp/barcode-{}".format(options['id'])
        self.tmp_image_label = "./tmp/label-{}.png".format(options['id'])
        self.tmp_bin = "./tmp/{}.bin".format(options['id'])
        self.font_text = ImageFont.load_default()
        print(options['id'])
        obj_barcode = barcode.Code128(str(options['id']), writer=ImageWriter())
        obj_barcode.save(self.tmp_image)
        obj_output_image = Image.new('RGB', (self.int_label_width, self.int_label_height), color='white')
        obj_output_draw = ImageDraw.Draw(obj_output_image)
        int_width, int_height = obj_output_image.size
        int_text_width, int_text_height = obj_output_draw.textsize(options['center_text'], self.font_text)

        obj_barcode_image = Image.open("{}.png".format(self.tmp_image))
        obj_barcode_image.thumbnail((self.int_label_width, self.int_label_width), Image.ANTIALIAS)
        obj_barcode_image.save(self.tmp_image_label)
        int_image_width, int_image_height = obj_barcode_image.size
        obj_output_image.paste(obj_barcode_image,
                               (math.floor((int_width - int_image_width) / 2),
                                math.floor((int_height - int_image_height) / 2)))
        obj_barcode_image.close()
        obj_output_draw.text(
            (math.floor((int_width - int_text_width) / 2), int_height - int_text_height - 5),
            options['center_text'],
            (0, 0, 0), font=self.font_text)

        obj_output_image.save(self.tmp_image_label, "PNG")

        # if options['print']:
        #     subprocess.call(['brother_ql_create --model QL-800 --label-size {} --rotate 90 {} > {}'
        #                     .format(self.int_label_length, self.tmp_image_label, self.tmp_bin)])
        #     subprocess.call(['cat {} > {} '.format(self.tmp_bin, self.printer)])
