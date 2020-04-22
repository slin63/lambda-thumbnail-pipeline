# https://pillow.readthedocs.io/en/latest/handbook/tutorial.html#create-jpeg-thumbnails
from PIL import Image


def to_thumbnail(f, max_size=500):
    im = Image.open(f)
    im.thumbnail((max_size, max_size), Image.ANTIALIAS)
    im.save(f.name, "jpeg")
    return True
