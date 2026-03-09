import os
from datetime import date

import requests
import streamlit as st
from dotenv import load_dotenv
from streamlit_modal import Modal

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Meal Planner", page_icon="🍽️", layout="wide")

st.sidebar.title("Meal Planner")

if "users" not in st.session_state:
    try:
        response = requests.get(f"{API_BASE_URL}/api/users")
        st.session_state.users = response.json() if response.status_code == 200 else []
    except:
        st.session_state.users = []

if "selected_user" not in st.session_state:
    st.session_state.selected_user = None

if st.session_state.users:
    user_names = [u["name"] for u in st.session_state.users]
    selected_name = st.sidebar.selectbox("Select User", user_names)
    st.session_state.selected_user = next(
        u for u in st.session_state.users if u["name"] == selected_name
    )
else:
    st.sidebar.warning("No users found. Create users first!")

with st.sidebar.expander("Add New User"):
    with st.form("new_user"):
        name = st.text_input("Name")
        is_veg = st.checkbox("Vegetarian")
        protein = st.number_input(
            "Protein Target (g/day)", value=80, min_value=50, max_value=200
        )
        fiber = st.number_input(
            "Fiber Target (g/day)", value=30, min_value=20, max_value=60
        )

        if st.form_submit_button("Create User"):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/api/users",
                    json={
                        "name": name,
                        "is_vegetarian": is_veg,
                        "protein_target": protein,
                        "fiber_target": fiber,
                    },
                )
                if response.status_code == 200:
                    st.success(f"User {name} created!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

st.title("Home")

st.markdown(
    """
    <style>
    /* Target the modal dialog */
    section[data-testid="stLayoutWrapper"] {
        width: 80vw !important;           /* Width as % of viewport */
        max-width: 1000px !important;     /* Maximum width */
        height: 70vh !important;          /* Height as % of viewport */
        max-height: 800px !important;     /* Maximum height */
    }
    
    /* Center the modal */
    section[data-testid="stLayoutWrapper"] > div {
        position: fixed !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
    }
    
    /* Adjust modal content area */
    section[data-testid="stLayoutWrapper"] [data-testid="stVerticalBlock"] {
        height: 100%;
        overflow-y: auto;
    }
    </style>
""",
    unsafe_allow_html=True,
)

if st.session_state.selected_user:
    user = st.session_state.selected_user

    st.header(f"Welcome, {user['name']}!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Diet Type", "Vegetarian" if user["is_vegetarian"] else "Non-Vegetarian"
        )
    with col2:
        st.metric("Protein Target", f"{user['protein_target']}g/day")
    with col3:
        st.metric("Fiber Target", f"{user['fiber_target']}g/day")

    st.divider()

    st.subheader("Quick Actions")

    col1, col2 = st.columns(2)
    modal = Modal("Special Requirements", key="special_reqs_modal", max_width=1000)

    with col1:
        st.info(
            "Special requirements noted: "
            + st.session_state.get("special_requirements", "None")
        )
        if st.button("Generate Today's Meals", use_container_width=True):

            if not st.session_state.get("special_requirements_noted", False):
                modal.open()
            else:
                with st.spinner("Generating meals..."):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/api/meal-plans/generate/{user['id']}",
                            params={
                                "target_date": str(date.today()),
                                "special_requirements": st.session_state.get(
                                    "special_requirements", ""
                                ),
                            },
                        )
                        if response.status_code == 200:
                            st.success("Today's meals generated!")
                            st.balloons()
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Error: {e}")

    with col2:
        st.page_link(
            "pages/1_Meal_Plans.py", label="View Meal Plans", use_container_width=True
        )

    if modal.is_open() and not st.session_state.get(
        "special_requirements_noted", False
    ):
        with modal.container():
            sp_req = st.text_input(
                "Any special dietary requirements or preferences for today?",
                key="special_requirements_input",
            )
            if st.button("Submit", use_container_width=True):
                st.session_state.special_requirements = sp_req
                st.session_state.special_requirements_noted = True
                st.success("Special requirements noted!")
                modal.close()

    st.divider()

    st.info("""
    **Navigation:**
    - **Meal Plans**: View and manage your weekly meal schedule
    - **Inventory**: Track available ingredients
    - **History**: See your past week's meals and nutrition
    """)

else:
    st.info("Please select or create a user from the sidebar to get started!")
