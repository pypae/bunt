import math
from operator import itemgetter
from pathlib import Path

import cv2
import numpy as np

from bunt import crc
from bunt.constants import BGR_TO_COLORS, INSET, POSITIONS, SHAPES, WIDTH


def read_code(img: np.ndarray) -> int:
    margin = 24
    code = 0
    white_fill = (255,)
    no_border = -1

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    shape_mask = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]

    # We reverse the positions to make constructing the code easier by shifting right.
    # (When generating the code we shift left.)
    for i, (x, y) in enumerate(reversed(POSITIONS)):
        # Find the center of each quadrant (from bottom right)
        center = INSET + WIDTH // 4 + x * (WIDTH // 2), INSET + WIDTH // 4 + y * (
            WIDTH // 2
        )

        # Find the color of each quadrant:
        # We look at the average color of the pixels in a circle in the center of the quadrant.
        radius = WIDTH // 4 - margin
        mask = np.zeros(img.shape[:2], np.uint8)
        cv2.circle(mask, center, radius, white_fill, no_border)
        color = cv2.mean(img, mask=mask)[:3]
        # Find the closest color in our list of colors
        # We use the Euclidean distance in BGR space. TODO could be optimized
        distances = [
            (math.dist(color, rgb), (i, name))
            for i, (rgb, name) in enumerate(BGR_TO_COLORS.items())
        ]
        distance, (color_index, color_name) = min(distances, key=itemgetter(0))

        # Annotate the image for debugging
        cv2.circle(img, center, radius, (0, 0, 0), 2)
        cv2.putText(
            img,
            color_name,
            center,
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.3,
            color=(0, 0, 0),
        )

        # Find the shape of each quadrant:
        shape = [False] * 4
        for d in range(4):
            # We look at each corner of the quadrant and check if it is filled.
            # map from [0,1,2,3] to (-1, -1), (-1, 1), (1, -1), (1, 1)
            x_, y_ = 2 * (d & 1) - 1, 2 * (d >> 1) - 1
            p = center[0] + x_ * radius, center[1] + y_ * radius
            m = np.zeros(img.shape[:2], np.uint8)
            cv2.circle(m, p, 10, white_fill, no_border)
            color = cv2.mean(shape_mask, mask=m)[:1][0]
            filled = color < 240
            shape[d] = filled
            # Annotate the image for debugging
            cv2.putText(
                img,
                str(filled),
                p,
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.3,
                color=(0, 0, 0),
            )

        shape_index = SHAPES.index(tuple(shape))

        code = code << 4 | shape_index
        code = code << 3 | color_index

    return crc.get_message(code)


if __name__ == "__main__":
    media_ref = 12345678
    # Manually take a photo of the code and save it to samples/12345678.png
    # You can use `detect.py` to extract the code from samples/12345678_raw.png.
    in_file = Path(__file__).parent / f"../samples/{media_ref}.png"
    img = cv2.imread(str(in_file))
    img = cv2.resize(img, (560, 560), interpolation=cv2.INTER_AREA)
    try:
        print(read_code(img))
    except ValueError as e:
        print(e)
    annotated_file = Path(__file__).parent / f"../samples/{media_ref}_annotated.png"
    cv2.imwrite(str(annotated_file), img)
