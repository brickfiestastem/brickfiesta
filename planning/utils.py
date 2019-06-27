from PIL import Image
import math


def image_square(image_path, min_size=256, fill_color=(255, 0, 0, 0)):
    rectangle_image = Image.open(image_path)
    x, y = rectangle_image.size
    int_size = max(min_size, x, y)
    square_image = Image.new('RGBA', (int_size, int_size), fill_color)
    square_image.paste(rectangle_image, (int(
        (int_size - x) / 2), int((int_size - y) / 2)))
    rectangle_image.close()
    return square_image


class Table:

    def __int__(self, int_width=30, int_length=72, int_number=0):
        self.width = int_width
        self.length = int_length
        self.number = int_number
        self.moc_counter = 1
        self.table = [[0]*self.get_width_grid_units() for i in range(self.get_length_grid_units())]
        self.mocs = list()

    def get_length_grid_units(self):
        return math.floor(self.length / 5)

    def get_width_grid_units(self):
        return math.floor(self.width / 5)

    def get_grid_unit_area(self):
        return self.get_width_grid_units() * self.get_length_grid_units()

    def get_area(self):
        return self.length * self.width

    def get_table_usage(self):
        int_table_usage = 0
        for int_width in range(self.get_width_grid_units()):
            for int_length in range(self.get_length_grid_units()):
                if self.table[int_width][int_length] != 0:
                    int_table_usage += 1
        return int_table_usage

    def check_moc_space(self, int_start_width, int_start_length, int_end_width, int_end_length):
        for int_width in range(int_start_width, int_end_width):
            for int_length in range(int_start_length, int_end_length):
                if self.table[int_width][int_length] != 0:
                    return False
        return True
