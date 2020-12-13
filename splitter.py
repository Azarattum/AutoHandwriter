from math import ceil
from PIL import ImageFont
import random


def split(img, text, rescale=6):
    height, width, _ = img.shape
    width //= rescale
    height //= rescale

    fontpath = "./data/lorenco.ttf"
    size = ceil(height * 0.058)
    margin = width * 0.11

    font = ImageFont.truetype(fontpath, size)

    result = ""
    parts = text.split(" ")
    for part in parts:
        updated = result + part
        size = font.getsize(updated.split("\n")[-1 - part.count("\n")])[0]
        if (size < (width - margin * 2)):
            result += part + " "
        else:
            result += "\n" + part

    return result


def randomize(text):
    parts = text.split(" ")

    spaces = [" ", "  "]

    result = ""
    for part in parts:
        result += part + random.choices(spaces, weights=(30, 4))[0]

    parts = result.split("\n")
    spaces = ["", " "]

    result = ""
    for part in parts:
        result += part + "\n" + random.choices(spaces, weights=(30, 10))[0]

    return result.strip()
