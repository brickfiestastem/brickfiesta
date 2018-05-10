from PIL import Image


def image_square(image_path, min_size=256, fill_color=(255, 0, 0, 0)):
    rectangle_image = Image.open(image_path)
    x, y = rectangle_image.size
    int_size = max(min_size, x, y)
    square_image = Image.new('RGBA', (int_size, int_size), fill_color)
    square_image.paste(rectangle_image, (int((int_size - x) / 2), int((int_size - y) / 2)))
    rectangle_image.close()
    return square_image
