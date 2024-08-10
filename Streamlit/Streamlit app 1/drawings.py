import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

st.title("_:red[Varnika's personal art gallery]_:art:!")

col1, col2 = st.columns(2)
with col1:
   st.image("elephants_kalamkari.jpg", caption = 'Art piece 1')

with col2:
   st.header("Elegance in Tradition: A Kalamkari Tale of an Elephant Family")
   # Feedback form for first drawing
   rating1 = st.slider("Rate this drawing:memo:", 1, 5, key="rating1")
   comment1 = st.text_area("Any additional comments?", key="comment1", height=30)
   if st.button("Submit Feedback 1"):
      st.success("Thank you for your feedback!:sunglasses:")
   
col3, col4 = st.columns(2)
with col3:
   st.header("Swimming in Harmony: A Tale of Two Fishes")
   # Feedback form for second drawing
   rating2 = st.slider("Rate this drawing:memo:", 1, 5, key="rating2")
   comment2 = st.text_area("Any additional comments?", key="comment2", height=30)
   if st.button("Submit Feedback 2"):
      st.success("Thank you for your feedback!:sunglasses:")

with col4:
   st.image("fishes_kalamkari.jpg", caption = 'Art piece 2')


