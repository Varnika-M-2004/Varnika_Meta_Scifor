import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Analysis of Shoes sales!")

st.write("### Input Data")
col1, col2 = st.columns(2)
shoes_brand = col1.text_input("Shoes brand")
shoes_price = col1.number_input("Price")
shoes_category = col2.text_input("Male/Female")
shoes_size = col2.number_input("Shoe size", min_value=5, value=13)

#simulating a small dataset for demonstration
data = {
    'Brand': ['Nike', 'Adidas', 'Puma', 'Nike', 'Adidas'],
    'Price': [100, 150, 120, 130, 140],
    'Category': ['Male', 'Female', 'Male', 'Female', 'Male'],
    'Size': [10, 7, 9, 6, 8]
}

shoes_data = pd.DataFrame(data)

# Append user input to the dataframe
if shoes_brand and shoes_price and shoes_category and shoes_size:
    new_entry = pd.DataFrame({
        'Brand': [shoes_brand],
        'Price': [shoes_price],
        'Category': [shoes_category],
        'Size': [shoes_size]
    })
    shoes_data = pd.concat([shoes_data, new_entry], ignore_index = True)

#Display the data
st.write("### Shoes Sales Data")
st.dataframe(shoes_data)

# Data visualization
st.write("### Data Visualization")
fig, ax = plt.subplots(1, 2, figsize = (12,6))

#Price distribution
sns.histplot(shoes_data['Price'], kde = True, ax = ax[0])
ax[0].set_title("Price Distribution")

#Size Distribution
sns.histplot(shoes_data['Size'], kde=True, ax = ax[1])
ax[1].set_title("Size Distribution")

st.pyplot(fig)

#Statistical Summary
st.write("### Statistical Summary")
st.write(shoes_data.describe())

#Filtering options
st.write("### Filter Data")
filter_brand = st.selectbox("Select Brand", options=shoes_data['Brand'].unique())
filtered_df = shoes_data[shoes_data['Brand']==filter_brand]
st.write(filtered_df)

#Insights
st.write("### Insights")
avg_price = shoes_data['Price'].mean()
st.write(f"The average price of shoes is ${avg_price:.2f}")

if st.checkbox('Show Line plot'):
    fig, ax = plt.subplots()
    sns.lineplot(shoes_data)
    st.pyplot(fig)

#End of the app
st.write("Thank you for using the Shoes Sales Analysis app!")