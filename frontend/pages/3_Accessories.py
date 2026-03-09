import streamlit as st
import requests
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Accessories", page_icon="🛒", layout="wide")

st.title("Accessories Management")

st.info(
    "Track your available accessories. The meal generator will prioritize using these tools/accessories."
)

_, col_center, _ = st.columns([1, 2, 1])

with col_center:
    with st.form("add_accessory", clear_on_submit=True):
        st.subheader("Add Accessory")
        new_accessory = st.text_input(
            "Accessory name", placeholder="e.g., blender, oven, mixer"
        )
        accessory_desc = st.text_area(
            "Description (optional)",
            placeholder="Add a brief description of the accessory",
        )
        submit = st.form_submit_button("Add", use_container_width=True)

    if submit and new_accessory:
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/accessories",
                json={
                    "accessory_name": new_accessory.lower().strip(),
                    "description": accessory_desc.strip(),
                },
            )
            if response.status_code == 200:
                st.success(f"✅ Added {new_accessory}")
                st.rerun()
            else:
                st.error("Failed to add accessory")
        except Exception as e:
            st.error(f"Error: {e}")
            st.markdown(f"**{new_accessory.title()}**")

st.divider()

_, col_center, _ = st.columns([1, 2, 1])

with col_center:
    st.subheader("📋 Current Accessories")

    try:
        response = requests.get(f"{API_BASE_URL}/api/accessories")

        if response.status_code == 200:
            accessories = response.json()
            num_cols = 4

            if not accessories:
                st.info(
                    "Your accessories list is empty. Add some accessories to get started!"
                )
            else:
                # Display in a grid
                cols = st.columns(num_cols)
                for idx, accessory in enumerate(accessories):
                    with cols[idx % num_cols]:
                        st.markdown(f"**{accessory['accessory_name'].title()}**")
                        if accessory.get("description"):
                            st.markdown(f"*{accessory['description']}*")
                        delete_button = st.button(
                            "Delete", key=f"delete_{accessory['accessory_name']}"
                        )
                        if delete_button:
                            accessory_id = int(accessory["id"])
                            del_response = requests.delete(
                                f"{API_BASE_URL}/api/accessories/{accessory_id}"
                            )
                            if del_response.status_code == 200:
                                st.success(f"✅ Deleted {accessory['accessory_name']}")
                                st.rerun()
                            else:
                                st.error(
                                    f"Failed to delete {accessory['accessory_name']}"
                                )
        else:
            st.error("Failed to fetch accessories")
    except Exception as e:
        st.error(f"Error: {e}")
