from PIL import Image
import math
import logging

logger = logging.getLogger(__name__)


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

    def __int__(self):
        self.width = 30
        self.length = 60
        self.number = 1
        self.moc_counter = 0
        self.table = [[0]*self.get_width_grid_units()
                      for i in range(self.get_length_grid_units())]
        self.mocs = dict()

    def get_length_grid_units(self, int_length=None):
        if int_length is not None:
            return math.floor(int_length / 5)
        return math.floor(self.length / 5)

    def get_width_grid_units(self, int_width=None):
        if int_width is not None:
            return math.floor(int_width / 5)
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

    def add_moc(self, obj_moc):
        for int_width in range(self.get_width_grid_units()):
            for int_length in range(self.get_length_grid_units()):
                if self.table[int_width][int_length] is 0:
                    int_moc_table_width = int_width + \
                        self.get_width_grid_units(obj_moc.width) - 1
                    int_moc_table_length = int_length + \
                        self.get_length_grid_units(obj_moc.length) - 1
                    logger.debug("W: %i, L: %i, MW: %i ML: %i", int_width,
                                 int_length, int_moc_table_width, int_moc_table_length)
                    if int_moc_table_width < len(self.table) and int_moc_table_length < len(self.table[int_moc_table_width]) and self.check_moc_space(self.width, self.length, int_moc_table_width, int_moc_table_length):
                        self.moc_counter += 1
                        self.mocs[self.moc_counter] = obj_moc
                        for int_moc_width in range(int_moc_table_width):
                            for int_moc_length in range(int_moc_table_length):
                                self.table[int_moc_width][int_moc_table_length] = self.moc_counter
                        return True
        return False
