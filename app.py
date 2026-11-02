import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Configuration
st.set_page_config(
    page_title="Smart Retail Analyzer",
    page_icon="📊",
    layout="wide"
)
# Dashboard Header
st.title("📊 Smart Retail Sales & Business Intelligence Analyzer")

st.markdown("""
### Welcome to the Smart Retail Dashboard!
Explore retail sales, profit, customer segments and regional
performance through interactive charts and filters.
""")

st.divider()

# Load Dataset
df = pd.read_csv("data/cleaned_retail_sales.csv")

df["Order Date"] = pd.to_datetime(df["Order Date"])
# Date Range Filter
st.sidebar.header("Date Filter")

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range

    df = df[
        (df["Order Date"].dt.date >= start_date) &
        (df["Order Date"].dt.date <= end_date)
    ]

# Sidebar Filters
st.sidebar.header("Dashboard Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Filter Dataset
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]

# Calculate KPIs
total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

total_orders = filtered_df["Order ID"].nunique()

total_customers = filtered_df["Customer ID"].nunique()

# KPI Section
st.subheader("📌 Business Performance Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total Sales",
        value=f"${total_sales:,.2f}"
    )

with col2:
    st.metric(
        label="📈 Total Profit",
        value=f"${total_profit:,.2f}"
    )

with col3:
    st.metric(
        label="📦 Total Orders",
        value=f"{total_orders:,}"
    )

with col4:
    st.metric(
        label="👥 Total Customers",
        value=f"{total_customers:,}"
    )

st.divider()
# Category-wise Sales Chart
st.subheader("Category-wise Sales")

category_sales = filtered_df.groupby("Category")["Sales"].sum()

fig, ax = plt.subplots(figsize=(8, 4))

sns.barplot(
    x=category_sales.index,
    y=category_sales.values,
    ax=ax
)

ax.set_xlabel("Category")
ax.set_ylabel("Sales")

st.pyplot(fig)
# Category-wise Profit Analysis
st.subheader("Category-wise Profit")

category_profit = filtered_df.groupby("Category")["Profit"].sum()

fig, ax = plt.subplots(figsize=(8, 5))

sns.barplot(
    x=category_profit.index,
    y=category_profit.values,
    ax=ax
)

ax.set_xlabel("Category")
ax.set_ylabel("Total Profit")
ax.set_title("Profit Analysis by Category")

st.pyplot(fig)
plt.close(fig)

# Region-wise Sales Chart
st.subheader("Region-wise Sales")

region_sales = filtered_df.groupby("Region")["Sales"].sum()

fig, ax = plt.subplots(figsize=(8, 4))

sns.barplot(
    x=region_sales.index,
    y=region_sales.values,
    ax=ax
)

ax.set_xlabel("Region")
ax.set_ylabel("Sales")

st.pyplot(fig)

# Monthly Sales Trend
st.subheader("Monthly Sales Trend")

monthly_sales = filtered_df.groupby(
    filtered_df["Order Date"].dt.to_period("M")
)["Sales"].sum()

monthly_sales.index = monthly_sales.index.astype(str)

fig, ax = plt.subplots(figsize=(12, 4))

ax.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o"
)

ax.set_xlabel("Month")
ax.set_ylabel("Sales")
ax.tick_params(axis="x", rotation=90)

st.pyplot(fig)

# Sub-category Profit Analysis

st.subheader("Sub-Category-wise Profit")

subcategory_profit = filtered_df.groupby(
    "Sub-Category"
)["Profit"].sum().sort_values()

fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(
    x=subcategory_profit.values,
    y=subcategory_profit.index,
    ax=ax
)

ax.axvline(x=0, color="black", linestyle="--")
ax.set_xlabel("Total Profit")
ax.set_ylabel("Sub-Category")
ax.set_title("Profit Analysis by Product Sub-Category")

st.pyplot(fig)
plt.close(fig)

# Sub-Category-wise Sales
st.subheader("Sub-Category-wise Sales")

subcategory_sales = filtered_df.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(12, 5))

sns.barplot(
    x=subcategory_sales.index,
    y=subcategory_sales.values,
    ax=ax
)

ax.set_xlabel("Sub-Category")
ax.set_ylabel("Total Sales")
ax.tick_params(axis="x", rotation=45)

st.pyplot(fig)
# Customer Segment-wise Sales
st.subheader("Customer Segment-wise Sales")

segment_sales = filtered_df.groupby("Segment")["Sales"].sum()

fig, ax = plt.subplots(figsize=(8, 5))

sns.barplot(
    x=segment_sales.index,
    y=segment_sales.values,
    ax=ax
)

ax.set_xlabel("Customer Segment")
ax.set_ylabel("Total Sales")

st.pyplot(fig)
# Region-wise Profit
st.subheader("Region-wise Profit")

region_profit = filtered_df.groupby("Region")["Profit"].sum()

fig, ax = plt.subplots(figsize=(8, 5))

sns.barplot(
    x=region_profit.index,
    y=region_profit.values,
    ax=ax
)

ax.set_xlabel("Region")
ax.set_ylabel("Total Profit")

st.pyplot(fig)
plt.close(fig)

# Data Table
st.subheader("Retail Sales Dataset")

st.dataframe(filtered_df, width="stretch")

st.success("Dashboard loaded successfully!")
# Download Filtered Dataset
st.subheader("📥 Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Dataset",
    data=csv,
    file_name="filtered_retail_sales.csv",
    mime="text/csv"
)