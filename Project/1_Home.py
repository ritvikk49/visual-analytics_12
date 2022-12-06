import pandas as pd
import numpy as np
import streamlit as st
import requests
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner


st.set_page_config(
    page_title="Spotify Data Charts",
    page_icon="🎶",
)
st.title("Spotify DATA CHARTS")


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url = "https://assets7.lottiefiles.com/packages/lf20_ugylqlzx.json"
lottie_json = load_lottieurl(lottie_url)
st_lottie(lottie_json, speed=1, loop=True, quality="medium", width=300)

st.subheader("About Us")
st.markdown('This application is the work done by **Project Group 12** of the Visual Analytics class of Fall 2022 semester.')
st.markdown(
"""
The members of the group are:
- Sharaschandrika Nimma
- Pavan Kalyan Reddy Madatala
- Ritvik Kondabathini
- June Kathman
"""
)

st.subheader("Background")
st.markdown('This is a dataset of the "Top 200" chart published globally by Spotify. Spotify publishes a new chart every 2-3 days. The dataset we are considering here between the period of January 2019 and December 2020.')
st.markdown(
"""
The dataset has been reduced and transformed in the following way:
- It contains 6 attributes: **title, rank, date, artist, region, streams**
- It contains the Top200 charts for the 1st of every month for the years 2019, 2020 and 2021
- The total number of rows are **394743** and the total size of the dataset is **24.9 MB**
- The data types of the tuples across the dataset are **int64, float64, string (object) and datetime64**
"""
)

st.subheader("Approach and Uses")
st.markdown(
"""
<div style="text-align: justify;">We have created visualisations on the data based off of questions that were curated from the dataset to understand it better. These visualisation give us an answer in the best possible way.

The visualisations are on an introductory level of what can be further expanded to help firms and individuals understand the data and derive desired conclusions from it. Looking at the raw dataset cannot provide much understanding usless it is processed to a more visually appealing and easily understandable way. We have attempted to achieve this by making this application.</div>
""" , unsafe_allow_html=True)

