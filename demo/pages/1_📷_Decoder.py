# TODO get streamlit_webrtc working for live demo
import cv2
import numpy as np
import streamlit as st

from bunt.decode import read_code
from bunt.detect import detect_code, draw_contour, extract_code, threshold


def main():
    img_file_buffer = st.camera_input("Take a picture of a `bunt` code to decode")

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

Inspired by Spotify codes and [this blog post](https://boonepeter.github.io/posts/spotify-codes-part-2) in particular."""
)

st.header("Decoder")
main()
