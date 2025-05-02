import streamlit as st
import pandas as pd
import base64

# Load the dataset
def load_data():
    data = pd.read_csv("drug_interactions.csv")
    return data 

df = load_data()

# Function to convert image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Convert images to base64
img1 = get_base64_image("C:/Users/Windows 11/Desktop/Eng A/Project pharma/Project/1.jpg")
img2 = get_base64_image("C:/Users/Windows 11/Desktop/Eng A/Project pharma/Project/2.jpg")

# Display logos centered
st.markdown(
    f"""
    <div style='text-align: center; margin-bottom: 30px;'>
        <img src='data:image/png;base64,{img1}' width='100' style='margin-right: 40px;'/>
        <img src='data:image/png;base64,{img2}' width='100'/>
    </div>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("Welcome to the Smart Drug Safety Assistant")
st.write("This app helps pharmacists quickly check drug interactions and ensure medication safety.")
