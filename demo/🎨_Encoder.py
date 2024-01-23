import os

import streamlit as st

from bunt.encode import create_code

ENV = os.getenv("ENV", "development")
base_url = (
    "http://localhost:8501"
    if ENV == "development"
    else "https://bunt-codes.streamlit.app"
)

sidebar = st.sidebar

sidebar.title("Bunt")
sidebar.markdown(
    """Colorful, scannable QR-like codes. 🌈 

Inspired by Spotify codes and [this blog post](https://boonepeter.github.io/posts/spotify-codes-part-2) in particular.


**But Why?** Because they look cool and I wanted to learn the basics of image processing and computer vision."""
)


st.header("Encoder")

input = st.number_input(
    "Enter a number to encode",
    help='"bunt" allows to encode values between 0 and 2**25',
    value=12345678,
    min_value=0,
    max_value=2**25,
)
code = create_code(input)
svg = code.as_svg()
st.image(svg, use_column_width="always", caption=f"Encoded value: {input}")
st.markdown(f"Decode on another device: [{base_url}/Decoder]({base_url}/Decoder)")

st.markdown(
    """### How the encoder works
"bunt" codes allow to encode 28 bits of data. 
3 of these bits are used by an error detecting code, while the remaining 25 bits can be used to encode data.

The data is encoded as follows:
1. Take a number between `0` and `33554432` (`2**25`)
1. Compute the 3-bit error detecting code of this number. 
  Inspired by Spotify codes, we use a [cyclic redundancy check](https://en.wikipedia.org/wiki/Cyclic_redundancy_check) (CRC) with the polynomial `0b1011`.
  For implementation details see [`bunt/crc.py`](https://github.com/pypae/bunt/blob/main/bunt/crc.py).
  The bits of the error detecting code are appended to the bits of the number, resulting in 28 bits of data.
1. Split the 28 bits into 4 groups of 7 bits. 
  Each group of 7 bits encodes to one quadrant of the code. 
  We use 8 visually distinct colors, so we need 3 bits per color.
  The remaining 4 bits encode the shape of the quadrant.
  We use a square where each of the four corners can be rounded off or not, resulting in 16 possible shapes.
1. Add a white background to the code to make it easier to detect.

For implementation details see [`bunt/encode.py`](https://github.com/pypae/bunt/blob/main/bunt/encode.py).

### Things to try next
- [ ] Add an indicator for the orientation of the code. (E.g. a dot in the top right quadrant.)
- [ ] Use an error *correcting* code instead or in addition to an error *detecting* code.
- [x] Shuffle the bits after adding the error detecting code. 
  This would make the code more robust against errors that affect a whole quadrant.
"""
)
