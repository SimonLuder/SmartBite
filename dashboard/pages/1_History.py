import streamlit as st

st.set_page_config(page_title="History", page_icon="🍽️")

st.title("Analysis History")

history = st.session_state.get("history", [])


if not history:
    st.info("You haven't analyzed any meals yet.")
else:
    for i, entry in enumerate(reversed(history)):
        st.subheader(f"Meal #{len(history) - i}")

        st.image(entry["image"], width=200)

        col1, col2 = st.columns(2)
        col1.metric("Label", entry.get("label", "Unknown"))
        col2.metric("Confidence", f"{entry.get('confidence', 0) * 100:.2f}%")

        nutrition = entry.get("nutrition", {})
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Calories", f"{nutrition.get('calories', '?')} kcal")
        col2.metric("Protein", f"{nutrition.get('protein', '?')} g")
        col3.metric("Carbs", f"{nutrition.get('carbohydrates', '?')} g")
        col4.metric("Fat", f"{nutrition.get('fat', '?')} g")

        st.divider()

if st.button("🗑️ Clear History"):
    st.session_state["history"] = []
    st.rerun()