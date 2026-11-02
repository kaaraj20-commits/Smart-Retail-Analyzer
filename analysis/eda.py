
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned dataset
df = pd.read_csv("data/cleaned_retail_sales.csv", encoding="utf-8")
df["Order Date"] = pd.to_datetime(df["Order Date"])

# 1. Total Sales
total_sales = df["Sales"].sum()

# 2. Total Profit
total_profit = df["Profit"].sum()

# 3. Total Orders
total_orders = df["Order ID"].nunique()

# 4. Total Customers
total_customers = df["Customer ID"].nunique()

# 5. Total Products Sold
total_quantity = df["Quantity"].sum()

# Display results
print("========== RETAIL BUSINESS ANALYSIS ==========")

print("Total Sales:", round(total_sales, 2))
print("Total Profit:", round(total_profit, 2))
print("Total Orders:", total_orders)
print("Total Customers:", total_customers)
print("Total Products Sold:", total_quantity)

print("==============================================")
# CATEGORY-WISE SALES ANALYSIS

category_sales = df.groupby("Category")["Sales"].sum()
category_profit = df.groupby("Category")["Profit"].sum()

print("\nCATEGORY-WISE SALES:")
print(category_sales)

# Highest sales category
print("\nHIGHEST SALES CATEGORY:")
print(category_sales.idxmax())

# Highest profit category
print("\nHIGHEST PROFIT CATEGORY:")
print(category_profit.idxmax())

# REGION-WISE SALES ANALYSIS

region_sales = df.groupby("Region")["Sales"].sum()

print("\nREGION-WISE SALES:")
print(region_sales)

# Region-wise profit
region_profit = df.groupby("Region")["Profit"].sum()

print("\nREGION-WISE PROFIT:")
print(region_profit)

# Highest sales region
print("\nHIGHEST SALES REGION:")
print(region_sales.idxmax())

# Highest profit region
print("\nHIGHEST PROFIT REGION:")
print(region_profit.idxmax())

# SUB-CATEGORY-WISE SALES ANALYSIS

subcategory_sales = df.groupby("Sub-Category")["Sales"].sum()

print("\nSUB-CATEGORY-WISE SALES:")
print(subcategory_sales.sort_values(ascending=False))

# Sub-category-wise profit
subcategory_profit = df.groupby("Sub-Category")["Profit"].sum()

print("\nSUB-CATEGORY-WISE PROFIT:")
print(subcategory_profit.sort_values(ascending=False))

# Highest sales sub-category
print("\nHIGHEST SALES SUB-CATEGORY:")
print(subcategory_sales.idxmax())

# Highest profit sub-category
print("\nHIGHEST PROFIT SUB-CATEGORY:")
print(subcategory_profit.idxmax())

# MONTHLY SALES ANALYSIS

df["Month"] = df["Order Date"].dt.month
df["Year"] = df["Order Date"].dt.year

monthly_sales = df.groupby(["Year", "Month"])["Sales"].sum()

print("\nMONTHLY SALES:")
print(monthly_sales)

# Highest sales month
print("\nHIGHEST SALES MONTH:")
print(monthly_sales.idxmax())

# Lowest sales month
print("\nLOWEST SALES MONTH:")
print(monthly_sales.idxmin())
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

# Category-wise Sales Chart
st.subheader("📊 Category-wise Sales")

category_sales = filtered_df.groupby("Category")["Sales"].sum()

fig, ax = plt.subplots(figsize=(9, 5))

sns.barplot(
    x=category_sales.index,
    y=category_sales.values,
    ax=ax
)

ax.set_title("Total Sales by Product Category", fontsize=14, fontweight="bold")
ax.set_xlabel("Product Category")
ax.set_ylabel("Total Sales ($)")

ax.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, p: f"${x:,.0f}")
)

plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(fig)
plt.close(fig)
# Category-wise Profit Analysis
st.subheader("📈 Category-wise Profit")

category_profit = filtered_df.groupby("Category")["Profit"].sum()

fig, ax = plt.subplots(figsize=(9, 5))

sns.barplot(
    x=category_profit.index,
    y=category_profit.values,
    ax=ax
)

ax.set_title("Total Profit by Product Category", fontsize=14, fontweight="bold")
ax.set_xlabel("Product Category")
ax.set_ylabel("Total Profit ($)")

ax.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, p: f"${x:,.0f}")
)

plt.tight_layout()

st.pyplot(fig)
plt.close(fig)
   
# REGION-WISE SALES CHART

st.subheader("🌍 Region-wise Sales")

region_sales = filtered_df.groupby("Region")["Sales"].sum()

fig, ax = plt.subplots(figsize=(9, 5))

sns.barplot(
    x=region_sales.index,
    y=region_sales.values,
    ax=ax
)

ax.set_title("Total Sales by Region", fontsize=14, fontweight="bold")
ax.set_xlabel("Region")
ax.set_ylabel("Total Sales ($)")

ax.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, p: f"${x:,.0f}")
)

plt.tight_layout()

st.pyplot(fig)
plt.close(fig)
# MONTHLY SALES TREND CHART

st.subheader("📅 Monthly Sales Trend")

monthly_sales = filtered_df.groupby(
    filtered_df["Order Date"].dt.to_period("M")
)["Sales"].sum()

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    monthly_sales.index.astype(str),
    monthly_sales.values,
    marker="o"
)

ax.set_title(
    "Monthly Sales Trend",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Month")
ax.set_ylabel("Total Sales ($)")

ax.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, p: f"${x:,.0f}")
)

plt.xticks(rotation=90)
plt.tight_layout()

st.pyplot(fig)
plt.close(fig)
# SUB-CATEGORY-WISE PROFIT CHART

st.subheader("📦 Sub-Category-wise Profit")

subcategory_profit = filtered_df.groupby(
    "Sub-Category"
)["Profit"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(12, 6))

sns.barplot(
    x=subcategory_profit.index,
    y=subcategory_profit.values,
    ax=ax
)

ax.set_title(
    "Profit by Product Sub-Category",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Sub-Category")
ax.set_ylabel("Total Profit ($)")

ax.axhline(y=0, color="black", linestyle="--")

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)
plt.close(fig)
# CUSTOMER SEGMENT-WISE SALES CHART

st.subheader("👥 Customer Segment-wise Sales")

segment_sales = filtered_df.groupby("Segment")["Sales"].sum()

fig, ax = plt.subplots(figsize=(9, 5))

sns.barplot(
    x=segment_sales.index,
    y=segment_sales.values,
    ax=ax
)

ax.set_title(
    "Sales by Customer Segment",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Customer Segment")
ax.set_ylabel("Total Sales ($)")

ax.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, p: f"${x:,.0f}")
)

plt.tight_layout()

st.pyplot(fig)
plt.close(fig)