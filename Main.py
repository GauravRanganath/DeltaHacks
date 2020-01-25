import random
import string
from PIL import Image, ImageDraw


def randomizer():
    l = list(string.ascii_lowercase)
    l.pop(9)
    l.pop(24)
    return l[random.randint(0, 23)]

img = Image.open("ASL-Alphabets/" + randomizer() + ".jpg")
img.show()