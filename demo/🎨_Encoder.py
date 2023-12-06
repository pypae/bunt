import os

import streamlit as st

from bunt.encode import create_code

ENV = os.getenv("ENV", "development")
base_url = (
    "http://localhost:8501" if ENV == "development" else "https://bunt-codes.streamlit.app"
)

sidebar = st.sidebar

sidebar.title("Bunt")
sidebar.markdown(
    """Colorful, scannable QR-like codes. 🌈 

Inspired by Spotify codes and [this blog post](https://boonepeter.github.io/posts/spotify-codes-part-2) in particular."""
)


st.header("Encoder")
input = st.number_input(
    "Enter a number to encode",
    help="bunt allows to encode values between 0 and 2**25",
    value=12345678,
    min_value=0,
    max_value=2**25,
)
code = create_code(input)
html = code.as_html()
st.write(html, unsafe_allow_html=True)
st.markdown(f"Decode on another device: [{base_url}/Decoder]({base_url}/Decoder)")
