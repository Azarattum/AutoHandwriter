from handwriter import handwrite, apply_effects
from pdfminer.high_level import extract_text
from splitter import randomize, split
from os.path import basename
from detector import detect
from os import listdir
from math import ceil
from sys import argv
import numpy as np
import cv2 as cv
import re


def main():
    if (len(argv) < 2):
        print("Usage: py . <pdf>/validate")
        exit()
    source = argv[1]
    path = "./data/images/"
    validate = len(argv) >= 2 and argv[1] == "validate"

    images = [path + x for x in listdir(path)]
    img = cv.imread(images[0])

    if not validate:
        print("Processing the pdf (this might take a while)...")
        source = extract_text(source)
        source = re.sub("\n+", "\n", source).strip()
        source = randomize(source)
        source = split(img, source)
    else:
        print("Validating the dataset...")
    lines = source.split("\n")
    lines = list(filter(lambda line: len(str(line)) > 3, lines))

    # Lines per page
    lpp = 19
    total = ceil(len(lines) / lpp) if not validate else len(images)
    print("Pages will be generated: {}".format(total))

    for i, image in enumerate(images):
        img = cv.imread(image)

        text = "\n".join(lines[i * lpp:i * lpp + lpp])
        if (not text and not validate):
            break
        img, points = detect(img, validate)

        img, _ = handwrite(img, text, points)
        img = apply_effects(img)
        img = np.int0(img * 255)

        cv.imwrite("./out/{}".format(basename(image)), img)
        print("Generated: {}/{}    ".format(i + 1, total), end="\r")

    print("\nDone!")


main()
