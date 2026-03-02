import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# PAGE CONFIG
st.set_page_config(
    page_title="Performance Dashboard",
    layout="wide",
)

# LOAD DATA
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

category_cluster = pd.read_csv(os.path.join(BASE_DIR, "category_cluster.csv"))
avg_delivery = pd.read_csv(os.path.join(BASE_DIR, "avg_delivery_by_state.csv"))

# SIDEBAR
st.sidebar.header("Dashboard Settings")

top_n = st.sidebar.slider("Select Top N Categories", 5, 20, 10)

delivery_filter = st.sidebar.selectbox(
    "Filter Delivery Speed",
    ["All", "Fast (<10 days)", "Medium (10-20 days)", "Slow (>20 days)"]
)

# TITLE
st.title("Marketplace Performance Dashboard")
st.caption("12-Month Business Performance Overview")

st.divider()

# FILTER DATA
top_categories = (
    category_cluster
    .sort_values("Total_Orders", ascending=False)
    .head(top_n)
)

delivery_data = avg_delivery.copy()

if delivery_filter == "Fast (<10 days)":
    delivery_data = delivery_data[delivery_data["Avg_Delivery_Days"] < 10]
elif delivery_filter == "Medium (10-20 days)":
    delivery_data = delivery_data[
        (delivery_data["Avg_Delivery_Days"] >= 10) &
        (delivery_data["Avg_Delivery_Days"] <= 20)
    ]
elif delivery_filter == "Slow (>20 days)":
    delivery_data = delivery_data[delivery_data["Avg_Delivery_Days"] > 20]

# KPI SECTION
col1, col2, col3 = st.columns(3)

top_category = top_categories.iloc[0]
slowest_state = avg_delivery.sort_values("Avg_Delivery_Days", ascending=False).iloc[0]
fastest_state = avg_delivery.sort_values("Avg_Delivery_Days").iloc[0]

with col1:
    st.metric("Top Category", top_category["Category"])

with col2:
    st.metric("Orders (Top Category)", f"{top_category['Total_Orders']:,}")

with col3:
    st.metric("Slowest State", slowest_state["State"])

st.divider()

# CHART 1 - TOP CATEGORY
st.subheader("Category Demand Ranking")

fig1, ax1 = plt.subplots(figsize=(8, 6))

sorted_top = top_categories.sort_values("Total_Orders")

bars = ax1.barh(sorted_top["Category"], sorted_top["Total_Orders"])

ax1.set_xlabel("Total Orders")
ax1.set_title(f"Top {top_n} Categories by Order Volume")

st.pyplot(fig1)

# CHART 2 - DELIVERY TIME
st.subheader("Delivery Performance by State")

sorted_delivery = delivery_data.sort_values("Avg_Delivery_Days")

fig2, ax2 = plt.subplots(figsize=(8, 8))

ax2.barh(sorted_delivery["State"], sorted_delivery["Avg_Delivery_Days"])

ax2.set_xlabel("Average Delivery Time (Days)")
ax2.set_title("Average Delivery Time per State")

st.pyplot(fig2)

# INSIGHT SECTION
st.divider()

st.subheader("Executive Summary")

st.markdown(f"""
- Kategori dengan permintaan tertinggi adalah **{top_category['Category']}**
  dengan total **{top_category['Total_Orders']:,} orders**.
- State dengan pengiriman tercepat adalah **{fastest_state['State']}**.
- State dengan pengiriman paling lambat adalah **{slowest_state['State']}**.
- Distribusi demand menunjukkan konsentrasi tinggi pada beberapa kategori utama.
""")