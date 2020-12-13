import cv2 as cv
import numpy as np


def detect(img, validate=False, rescale=6):
    height, width, _ = img.shape
    width //= rescale
    height //= rescale
    img = cv.resize(img, (width, height))

    kernel = (5 * 6 // rescale + rescale % 2, 5 * 6 // rescale + rescale % 2)

    # Apply preprocessing
    processed = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    # cv.imwrite("demo/1.jpg", processed)
    processed = cv.GaussianBlur(processed, kernel, 2)
    # cv.imwrite("demo/2.jpg", processed)
    processed = cv.Canny(processed, 80, 80)
    # cv.imwrite("demo/3.jpg", processed)

    processed = cv.dilate(processed, np.ones(kernel), iterations=2)
    processed = cv.erode(processed, np.ones(kernel), iterations=1)
    # cv.imwrite("demo/4.jpg", processed)

    # Find the contour
    contours, _ = cv.findContours(
        processed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    biggest = np.array([])
    max_area = 0

    for contour in contours:
        area = cv.contourArea(contour)

        peri = cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, peri * 0.02, True)
        if (area > max_area and len(approx) == 4):
            biggest = approx
            max_area = area

    if (validate):
        cv.drawContours(img, contours, -1, (0, 255, 255), 1)
        cv.drawContours(img, [biggest], -1, (0, 0, 255), 3)
        return (img, np.array([]))
    biggest = biggest.reshape((4, 2))

    # cv.drawContours(img, contours, -1, (0, 255, 255), 1)
    # cv.drawContours(img, [biggest], -1, (0, 0, 255), 3)
    # cv.imwrite("demo/5.jpg", img)

    # Reorder points
    add = biggest.sum(1)
    points = np.zeros((4, 2))
    points[0] = biggest[np.argmin(add)]
    points[3] = biggest[np.argmax(add)]
    diff = np.diff(biggest, axis=1)
    points[1] = biggest[np.argmin(diff)]
    points[2] = biggest[np.argmax(diff)]

    return (img, points)
