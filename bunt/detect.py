from pathlib import Path

import cv2
import imutils
import numpy as np
from imutils.perspective import four_point_transform


def threshold(img: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)
    return thresh


def detect_code(img: np.ndarray) -> np.ndarray:
    thresh = threshold(img)
    contours = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    code_contour = None
    for cnt in contours:
        # approximate the contour
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        # if our approximated contour has four points, then we can
        # assume we have found the outline of the receipt
        if len(approx) == 4:
            code_contour = approx
            break

    return code_contour


def draw_contour(img: np.ndarray, contour: np.ndarray) -> np.ndarray:
    detected = img.copy()
    cv2.drawContours(detected, [contour], 0, (0, 255, 0), 3)
    return detected


def extract_code(img: np.ndarray, contour: np.ndarray) -> np.ndarray:
    warped = four_point_transform(img.copy(), contour.reshape(4, 2))
    return warped


if __name__ == "__main__":
    media_ref = 12345678
    sample_file = Path(__file__).parent / f"../samples/{media_ref}_raw.png"
    img = cv2.imread(str(sample_file))
    contour = detect_code(img)
    if contour is not None:
        img_contour = draw_contour(img, contour)
        contour_file = Path(__file__).parent / f"../samples/{media_ref}_contour.png"
        cv2.imwrite(str(contour_file), img_contour)
        out_file = Path(__file__).parent / f"../samples/{media_ref}.png"
        img_warped = extract_code(img, contour)
        cv2.imwrite(str(out_file), img_warped)
