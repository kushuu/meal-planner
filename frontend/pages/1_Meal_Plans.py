import streamlit as st
import httpx
from datetime import date, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Meal Plans", page_icon="📅", layout="wide")


if 'selected_user' not in st.session_state or not st.session_state.selected_user:
    st.warning("Please select a user from the home page first!")
    st.stop()

st.title(f"📅 Meal Plans for {st.session_state.selected_user['name'].title()}")
user = st.session_state.selected_user

# Date range selector
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    start_date = st.date_input("From", value=date.today() - timedelta(days=3))
with col2:
    end_date = st.date_input("To", value=date.today() + timedelta(days=3))
with col3:
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

st.divider()

# Fetch meal plans
try:
    response = httpx.get(
        f"{API_BASE_URL}/api/meal-plans/user/{user['id']}",
        params={
            "start_date": str(start_date),
            "end_date": str(end_date)
        }
    )

    if response.status_code == 200:
        meal_plans = response.json()

        if not meal_plans:
            st.info("No meal plans found for this date range. Generate some meals!")
        else:
            # Group by date
            from collections import defaultdict
            plans_by_date = defaultdict(list)
            for plan in meal_plans:
                plans_by_date[plan['date']].append(plan)

            # Display meals day by day
            for plan_date in sorted(plans_by_date.keys()):
                is_today = plan_date == str(date.today())
                date_label = "📍 TODAY" if is_today else plan_date

                with st.expander(f"**{date_label}**", expanded=is_today):
                    daily_plans = plans_by_date[plan_date]

                    cols = st.columns(3)
                    for idx, plan in enumerate(sorted(daily_plans, key=lambda x: ['breakfast', 'lunch', 'dinner'].index(x['meal_type']))):
                        with cols[idx]:
                            meal_type = plan['meal_type'].capitalize()
                            emoji = {"breakfast": "🌅", "lunch": "☀️",
                                     "dinner": "🌙"}.get(plan['meal_type'], "🍽️")

                            st.markdown(f"### {emoji} {meal_type}")

                            if plan['eaten_outside']:
                                st.warning("🏪 Eaten Outside")
                                if st.button(f"Mark as Home Cooked", key=f"home_{plan['id']}"):
                                    httpx.patch(
                                        f"{API_BASE_URL}/api/meal-plans/{plan['id']}/eaten-outside",
                                        params={"eaten_outside": False}
                                    )
                                    st.rerun()
                            elif plan['meal_id']:
                                # Fetch meal details
                                meal_response = httpx.get(
                                    f"{API_BASE_URL}/api/meals/{plan['meal_id']}")
                                if meal_response.status_code == 200:
                                    meal = meal_response.json()

                                    st.markdown(f"**{meal['name']}**")
                                    st.caption(meal['description'])

                                    # Nutrition info
                                    st.markdown("**Nutrition:**")
                                    st.markdown(
                                        f"- 🥩 Protein: {meal['protein']}g")
                                    st.markdown(f"- 🌾 Fiber: {meal['fiber']}g")
                                    st.markdown(
                                        f"- 🔥 Calories: {meal['calories']}")

                                    # Ingredients
                                    with st.expander("📝 Ingredients"):
                                        for ing in meal['ingredients']:
                                            st.markdown(
                                                f"- {ing['quantity']} {ing['unit']} {ing['name']}")

                                    # Instructions
                                    if meal.get('instructions'):
                                        with st.expander("👨‍🍳 Instructions"):
                                            st.markdown(meal['instructions'])

                                    # Mark as eaten outside
                                    if st.button(f"Mark as Eaten Outside", key=f"outside_{plan['id']}"):
                                        httpx.patch(
                                            f"{API_BASE_URL}/api/meal-plans/{plan['id']}/eaten-outside",
                                            params={"eaten_outside": True}
                                        )
                                        st.rerun()
                            else:
                                st.info("No meal planned")

                    st.divider()
    else:
        st.error("Failed to fetch meal plans")

except Exception as e:
    st.error(f"Error: {e}")

# Generate meals button
st.divider()
st.subheader("Generate New Meals")

gen_col1, gen_col2 = st.columns([3, 1])

with gen_col1:
    gen_date = st.date_input("Generate meals for date:", value=date.today())
with gen_col2:
    if st.button("🎲 Generate", use_container_width=True):
        with st.spinner("Generating meals... This may take a minute."):
            try:
                response = httpx.post(
                    f"{API_BASE_URL}/api/meal-plans/generate/{user['id']}",
                    params={"target_date": str(gen_date)},
                    timeout=300
                )
                if response.status_code == 200:
                    st.success("✅ Meals generated!")
                    st.rerun()
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")
