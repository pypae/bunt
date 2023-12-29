# TODO get streamlit_webrtc working for live demo
import cv2
import numpy as np
import streamlit as st

from bunt.decode import read_code
from bunt.detect import detect_code, draw_contour, extract_code, threshold


def main():
    img_file_buffer = st.camera_input('Take a picture of a "bunt" code to decode')

    if img_file_buffer is None:
        return

    bytes_data = img_file_buffer.getvalue()
    img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    thresh = threshold(img)
    thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    debug = st.expander("Intermediate steps for debugging")
    debug.image(
        thresh, use_column_width=True, channels="BGR", caption="Thresholded image"
    )

    contour = detect_code(img)
    if contour is None:
        st.warning("No code detected.")
        return

    img_contour = draw_contour(img, contour)
    debug.image(
        img_contour, use_column_width=True, channels="BGR", caption="Detected contour"
    )

    img_warped = extract_code(img, contour)
    debug.image(
        img_warped, use_column_width=True, channels="BGR", caption="Extracted code"
    )

    # Resize to 560x560
    img_in = cv2.resize(img_warped, (560, 560), interpolation=cv2.INTER_AREA)

    result = None
    try:
        result = read_code(img_in)
    except ValueError as e:
        st.warning(str(e))

    debug.image(img_in, use_column_width=True, channels="BGR", caption="Annotated code")
    if result is not None:
        st.success(f"Decoded value: {result}")


sidebar = st.sidebar

sidebar.title("Bunt")
sidebar.markdown(
    """Colorful, scannable QR-like codes. 🌈 

Inspired by Spotify codes and [this blog post](https://boonepeter.github.io/posts/spotify-codes-part-2) in particular.

**But Why?** Because they look cool and I wanted to learn the basics of image processing and computer vision."""
)

st.header("Decoder")
main()

st.markdown(
    """
### How the decoder works
The decoder consists of the following steps:
1. Find the code in the image. 
  The detection algorithm is simple and not very robust. 
  We look for the largest square contour in the image.
  It is largely inspired by [this tutorial](https://pyimagesearch.com/2021/10/27/automatically-ocring-receipts-and-scans/).
  For implementation details see [`bunt/detect.py`](https://github.com/pypae/bunt/blob/main/bunt/detect.py).
1. Transform the detected area to a 560x560 pixel image.
1. Detect the color and shape of each quadrant of the code.
  To detect the color, we average the color of the pixels around a circle in the center of the quadrant.
  We then compute the euclidian distance to the list of known colors and pick the closest one.
  To detect the shape, we look at each corner of the quadrant and check if it is filled.
  See the debug output above for an example.
  For implementation details see [`bunt/decode.py`](https://github.com/pypae/bunt/blob/main/bunt/decode.py).
1. Verify the CRC and extract the original data.

### Things to try next
- Reduce the error rate in color detection by adjusting color balance and/or using a different color space.
- Improve the detection algorithm. (E.g. use a neural network.)
"""
)
