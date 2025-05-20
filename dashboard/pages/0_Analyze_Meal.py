import streamlit as st
from api import analyze_image

st.set_page_config(page_title="Analyze Meal", page_icon="🔍")

st.title("Analyze Your Meal")
st.divider()

# Initialize
if "current_image" not in st.session_state:
    st.session_state["current_image"] = None
if "history" not in st.session_state:
    st.session_state["history"] = []

# Define upload dialog
@st.dialog("📁 Upload Picture")
def upload_dialog():
    uploaded_file = st.file_uploader("Upload a photo of your meal", type=["jpg", "jpeg", "png"], accept_multiple_files=False, key="upload_file")
    if uploaded_file:
        st.session_state["current_image"] = uploaded_file
        st.rerun()

# Define camera dialog
@st.dialog("📷 Take Photo")
def camera_dialog():
    camera_file = st.camera_input("Take a photo of your meal", key="camera_input")
    if camera_file:
        st.session_state["current_image"] = camera_file
        st.rerun()

st.markdown("### Upload or Capture a Photo of your Meal", )
# Launch modals
col1, col2 = st.columns(2)
with col1:
    st.button("📁 Upload Picture", on_click=upload_dialog)
with col2:
    st.button("📷 Take Photo", on_click=camera_dialog)

# Show image and analyze
if st.session_state["current_image"]:
    st.image(st.session_state["current_image"], caption="Your Meal", use_container_width=True)

    if st.button("Submit"):
        with st.spinner("Analyzing your meal..."):
            # get result from API
            result = analyze_image(st.session_state["current_image"])
        if result.get("label") == "Error":
            st.error("Error analyzing image.")
        else:
            st.success("Analysis complete!")
        st.divider()
        # Save the result to history
        st.session_state["history"].append({
            "image": st.session_state["current_image"],
            "label": result.get("label").strip('", '),
            "confidence": result.get("probability"),
            "nutrition": result.get("nutrition")
        })

        # Show result
        col1, col2 = st.columns(2)
        col1.metric("Label", result.get("label", "Unknown").strip('", '))
        col2.metric("Confidence", f"{result.get('probability', '?') * 100:.2f}%")

        nutrition = result.get("nutrition", {})
        st.markdown(f"### Nutrition Information {(nutrition.get('serving_size', '?').lower())}")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Calories", f"{nutrition.get('calories', '?')}")
        col2.metric("Protein", f"{nutrition.get('protein', '?')}")
        col3.metric("Carbs", f"{nutrition.get('carbohydrates', '?')}")
        col4.metric("Fat", f"{nutrition.get('fat', '?')}")
        st.link_button("View Full Nutrition Info", nutrition.get("food_url", "#"), disabled=(nutrition.get("food_url", "#") == '#'))
        st.divider()


        # Clear the current image after analysis
        st.session_state["current_image"] = None
        st.session_state["camera_input"] = None
        st.session_state["upload_file"] = None
