import streamlit as st
import requests
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Meal Planner",
    page_icon="🍽️",
    layout="wide"
)

st.sidebar.title("Meal Planner")

if 'users' not in st.session_state:
    try:
        response = requests.get(f"{API_BASE_URL}/api/users")
        print('Got response from /api/users:', response.status_code)
        st.session_state.users = response.json() if response.status_code == 200 else []
    except:
        st.session_state.users = []

if 'selected_user' not in st.session_state:
    st.session_state.selected_user = None

if st.session_state.users:
    user_names = [u['name'] for u in st.session_state.users]
    selected_name = st.sidebar.selectbox("Select User", user_names)
    st.session_state.selected_user = next(
        u for u in st.session_state.users if u['name'] == selected_name)
else:
    st.sidebar.warning("No users found. Create users first!")

with st.sidebar.expander("Add New User"):
    with st.form("new_user"):
        name = st.text_input("Name")
        is_veg = st.checkbox("Vegetarian")
        protein = st.number_input(
            "Protein Target (g/day)", value=80, min_value=50, max_value=200)
        fiber = st.number_input("Fiber Target (g/day)",
                                value=30, min_value=20, max_value=60)

        if st.form_submit_button("Create User"):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/api/users",
                    json={
                        "name": name,
                        "is_vegetarian": is_veg,
                        "protein_target": protein,
                        "fiber_target": fiber
                    }
                )
                if response.status_code == 200:
                    st.success(f"User {name} created!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

st.title("Home")

if st.session_state.selected_user:
    user = st.session_state.selected_user

    st.header(f"Welcome, {user['name']}!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Diet Type", "Vegetarian" if user['is_vegetarian'] else "Non-Vegetarian")
    with col2:
        st.metric("Protein Target", f"{user['protein_target']}g/day")
    with col3:
        st.metric("Fiber Target", f"{user['fiber_target']}g/day")

    st.divider()

    st.subheader("Quick Actions")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate Today's Meals", use_container_width=True):
            with st.spinner("Generating meals..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/api/meal-plans/generate/{user['id']}",
                        params={"target_date": str(date.today())}
                    )
                    if response.status_code == 200:
                        st.success("Today's meals generated!")
                        st.balloons()
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

    with col2:
        st.page_link("pages/1_Meal_Plans.py",
                     label="View Meal Plans", use_container_width=True)

    st.divider()

    st.info("""
    **Navigation:**
    - **Meal Plans**: View and manage your weekly meal schedule
    - **Inventory**: Track available ingredients
    - **History**: See your past week's meals and nutrition
    """)

else:
    st.info("Please select or create a user from the sidebar to get started!")
