import streamlit as st
import pandas as pd
import requests as r
from bs4 import BeautifulSoup
import ast

st.title('Web Scraper Example')

# 1. Inputs
URL = st.text_input(label="Enter URL", value="https://old.reddit.com/r/learnpython/")

# Example Dictionary: Key is the 'Label', Value is the 'CSS Class'
default_dict = "{'titles': 'title', 'users': 'author'}"
ELEMENTS = st.text_area(label="Enter element dictionary (Target Classes)", value=default_dict)

if st.button(label="Scrape Site"):
    try:
        # Convert string to dict
        ELEMENT_DICT = ast.literal_eval(ELEMENTS)
        
        st.write(f"Scraping: {URL}...")

        # 2. The "Stealth" Header (Crucial for Reddit)
        # A more complete "Human" header set
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1', # Do Not Track
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # 3. Fetch Data
        response = r.get(URL, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = {}

            # 4. Parse based on your Dictionary
            for label, css_class in ELEMENT_DICT.items():
                # Find all elements with that class and get their text
                found_elements = soup.find_all(class_=css_class)
                results[label] = [el.get_text() for el in found_elements]

            # 5. Display as a Dataframe
            # We use try/except here in case the lists are different lengths
            df = pd.DataFrame.from_dict(results, orient='index').transpose()
            st.success("Scrape Complete!")
            st.dataframe(df)
            
        else:
            st.error(f"Failed to reach site. Status Code: {response.status_code}")

    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Check if your dictionary format is correct! e.g. {'name': 'class_name'}")