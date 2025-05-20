import streamlit as st
from pathlib import Path
from api import check_status


st.set_page_config(
    page_title="SmartBite",
    page_icon="🍽️",
    initial_sidebar_state="expanded",
)

st.title("Welcome to SmartBite! 🍽️")
st.subheader("Your AI-Powered Meal Analysis Assistant")

st.divider()


upload_img = Path(__file__).parent / "assets" / "upload_photo.jpg"
analyse_img = Path(__file__).parent / "assets" / "ai_analyse.png"

st.header("How it works:")
st.subheader("1. Upload a photo of your meal.")
st.image(upload_img, width=500)
st.divider()
st.subheader("2. Our AI analyzes the image.")
st.image(analyse_img, width=500)
st.divider()
st.subheader("3. Receive a detailed nutritional breakdown.")

col1, col2 = st.columns(2)
col1.metric("Label", "Burger")
col2.metric("Confidence", f"{99.99:.2f}%")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Calories", "500 kcal")
col2.metric("Protein", "15 g")
col3.metric("Carbs", "60 g")
col4.metric("Fat", "20 g")



