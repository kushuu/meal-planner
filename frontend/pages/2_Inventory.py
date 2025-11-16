import streamlit as st
import requests
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Inventory", page_icon="🛒", layout="wide")

st.title("Inventory Management")

st.info("Track your available ingredients. The meal generator will prioritize using these items.")

_, col_center, _ = st.columns([1, 2, 1])

with col_center:
    with st.form("add_item", clear_on_submit=True):
        st.subheader("Add Item")
        new_item = st.text_input(
            "Item name", placeholder="e.g., tomatoes, chicken, quinoa")
        quantity = st.number_input("Quantity", min_value=0, step=1)
        unit = st.text_input(
            "Unit (optional)", placeholder="e.g., grams, pieces, cups")
        submit = st.form_submit_button("Add", use_container_width=True)

    if quantity <= 0 and submit:
        st.error("Please enter a quantity greater than zero.")

    if submit and new_item and quantity > 0:
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/inventory",
                json={"item_name": new_item.lower().strip()}
            )
            if response.status_code == 200:
                st.success(f"✅ Added {new_item}")
                st.rerun()
            else:
                st.error("Failed to add item")
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()

# Display inventory
st.subheader("📋 Current Inventory")

try:
    response = requests.get(f"{API_BASE_URL}/api/inventory")

    if response.status_code == 200:
        items = response.json()
        num_cols = 3

        if not items:
            st.info("Your inventory is empty. Add some items to get started!")
        else:
            # Display in a grid
            cols = st.columns(num_cols)
            for idx, item in enumerate(items):
                with cols[idx % num_cols]:
                    with st.container():
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.markdown(f"**{item['item_name'].title()}**")
                        with col_b:
                            if st.button("🗑️", key=f"del_{item['id']}", help="Delete"):
                                requests.delete(
                                    f"{API_BASE_URL}/api/inventory/{item['id']}")
                                st.rerun()

            st.divider()
            st.caption(f"Total items: {len(items)}")
    else:
        st.error("Failed to fetch inventory")

except Exception as e:
    st.error(f"Error: {e}")

# Tips
st.divider()
st.markdown("""
### 💡 Tips
- Keep your inventory updated for better meal suggestions
- The meal generator will try to use available ingredients
- Coming in Phase 2: quantity tracking and expiry dates
""")
