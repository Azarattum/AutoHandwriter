import numpy as np
import cv2 as cv
from math import ceil
from PIL import ImageFont, ImageDraw, Image


def overlay_transparent(background, overlay):
    background_width = background.shape[1]
    background_height = background.shape[0]

    if 0 >= background_width or 0 >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if w > background_width:
        w = background_width
        overlay = overlay[:, :w]

    if h > background_height:
        h = background_height
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1],
                         1), dtype=overlay.dtype) * 255
            ],
            axis=2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[:h, :w] = (1.0 - mask) * \
        background[:h, :w] + mask * overlay_image

    return background


def handwrite(img, text, points, offset=0):
    if (not len(points)):
        return img, offset
    height, width, _ = img.shape

    # Draw text
    fontpath = "./data/lorenco.ttf"
    size = ceil(height * 0.058)
    margin = (width * 0.11, offset or height / 20 * 1.25)

    font = ImageFont.truetype(fontpath, size)
    offset = (margin[1] if offset == 0 else 0) + get_height(img, text)

    img_pil = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img_pil)
    draw.text(margin, text, font=font, fill=(82, 32, 0, 180))
    txt = np.array(img_pil)

    # cv.imwrite("demo/6.jpg", txt)

    source = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    target = np.float32(points)
    matrix = cv.getPerspectiveTransform(source, target)
    txt = cv.warpPerspective(txt, matrix, (width, height))
    # cv.imwrite("demo/7.jpg", txt)

    overlay_transparent(img, txt)
    # cv.imwrite("demo/8.jpg", img)

    return (img, offset)


def get_height(img, text):
    height = img.shape[0]
    fontpath = "./data/lorenco.ttf"
    size = ceil(height * 0.058)
    font = ImageFont.truetype(fontpath, size)

    return ceil(font.getsize(text)[1] * len(text.split("\n")) * 0.8)


def apply_effects(img):
    # Post processing
    img = cv.GaussianBlur(img, (3, 3), 0.6)

    row, col, _ = img.shape
    gaussian = np.random.random((row, col, 1)).astype(np.float32)
    gaussian = np.concatenate((gaussian, gaussian, gaussian), axis=2)
    img = cv.addWeighted(np.float32(
        img) / 255, 0.9, 0.25 * gaussian, 0.25, 0)

    return img
