import streamlit as st
import pandas as pd
import numpy as np
import requests as r

st.title('Webscaper Example')

url = st.text_input(label="Enter URL", placeholder="https://www.reddit.com/r/learnpython/")

elements = st.text_area(label="Enter element dict",
             placeholder="""{

}""")

if st.button(label="Scrape Site"):
    st.write("Scraping Site...")

    st.write(url)
    st.write(elements)