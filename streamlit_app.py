import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
sales_data = pd.read_csv("Sales Data.csv")
product_data = pd.read_csv("Product Data.csv")
customer_data = pd.read_csv("Customer Data.csv")
region_data = pd.read_csv("Region Data.csv")

# Step 2: Merge Data
# Merge Sales Data with Customer Data on Sales ID and Customer ID
merged_data = sales_data.merge(customer_data, left_on="Sales ID", right_on="Customer ID", how="left")
# Retain the Region column from Sales Data
merged_data["Region"] = sales_data["Region"]

# Merge the result with Product Data on Product ID
merged_data = merged_data.merge(product_data, on="Product ID", how="left")

# Merge the result with Region Data on Region
if "Region" in merged_data.columns:
    merged_data = merged_data.merge(region_data, on="Region", how="left")
else:
    st.error("The Region column is missing in the merged data!")

# Add a heading
st.title("Sales Analysis")

# Sidebar Filters
st.sidebar.header("Filters")
selected_region = st.sidebar.multiselect("Select Region", merged_data["Region"].unique(), default=list(merged_data["Region"].unique()))
selected_product = st.sidebar.multiselect("Select Product Category", merged_data["Product Category"].unique(), default=list(merged_data["Product Category"].unique()))
selected_gender = st.sidebar.multiselect("Select Gender", merged_data["Gender"].unique(), default=list(merged_data["Gender"].unique()))

# Handle case when no filters are selected (i.e., take all data)
if not selected_region:
    selected_region = list(merged_data["Region"].unique())
if not selected_product:
    selected_product = list(merged_data["Product Category"].unique())
if not selected_gender:
    selected_gender = list(merged_data["Gender"].unique())

# Filter the merged data based on the selected filters
filtered_data = merged_data[
    (merged_data["Region"].isin(selected_region)) &
    (merged_data["Product Category"].isin(selected_product)) &
    (merged_data["Gender"].isin(selected_gender))
]

# Step 3: Regional Sales Comparison
st.subheader("Regional Sales Comparison")

# Group data by Region and calculate total Sales Amount
region_sales = filtered_data.groupby("Region")["Sales Amount"].sum().reset_index()

# Plot bar chart using Plotly (for hover effect)
fig = px.bar(region_sales, x="Region", y="Sales Amount", 
             title="Total Sales by Region", 
             labels={"Sales Amount": "Sales Amount", "Region": "Region"},
             hover_data=["Sales Amount"])

# Display the plot in Streamlit
st.plotly_chart(fig)

# Step 4: Product Category Sales
st.subheader("Product Category Sales Distribution")

# Group data by Product Category and calculate total Sales Amount
category_sales = filtered_data.groupby("Product Category")["Sales Amount"].sum().reset_index()

# Plot Pie Chart using Plotly
fig = px.pie(category_sales, names="Product Category", values="Sales Amount", 
             title="Sales Distribution by Product Category",
             hover_data=["Product Category", "Sales Amount"])

# Display the plot in Streamlit
st.plotly_chart(fig)

# Step 5: Customer Demographics (Age vs Sales)
st.subheader("Customer Age vs Sales Amount")

# Group data by Age and calculate total Sales Amount for each age group
age_sales = filtered_data.groupby("Age")["Sales Amount"].sum().reset_index()

# Plot Scatter Plot using Plotly
fig = px.scatter(age_sales, x="Age", y="Sales Amount", 
                 title="Customer Age vs Sales Amount", 
                 labels={"Age": "Customer Age", "Sales Amount": "Total Sales Amount"},
                 hover_data=["Age", "Sales Amount"])

# Display the plot in Streamlit
st.plotly_chart(fig)


# Step 6: Quarterly Sales Trend
st.subheader("Quarterly Sales Trend")

# Convert Sales Date to datetime if not already in datetime format
merged_data["Sales Date"] = pd.to_datetime(merged_data["Sales Date"], errors='coerce')

# Define Quarters manually based on the given date ranges:
def assign_quarter(date):
    if pd.to_datetime("01-01-2022") <= date <= pd.to_datetime("01-08-2022"):
        return "Q1"
    elif pd.to_datetime("01-09-2022") <= date <= pd.to_datetime("01-16-2022"):
        return "Q2"
    elif pd.to_datetime("01-17-2022") <= date <= pd.to_datetime("01-24-2022"):
        return "Q3"
    elif pd.to_datetime("01-25-2022") <= date <= pd.to_datetime("02-01-2022"):
        return "Q4"
    else:
        return "Out of Range"  # Ensure no date falls out of the specified range

# Assign Quarters to the sales data
merged_data["Quarter"] = merged_data["Sales Date"].apply(assign_quarter)

# Group by Quarter and calculate total Sales Amount for each quarter
quarterly_sales = merged_data.groupby("Quarter")["Sales Amount"].sum().reset_index()

# Plot Line Chart using Plotly
fig = px.line(quarterly_sales, x="Quarter", y="Sales Amount", 
              title="Quarterly Sales Trend", 
              labels={"Quarter": "Quarter", "Sales Amount": "Total Sales Amount"},
              markers=True, line_shape="linear")

# Display the plot in Streamlit
st.plotly_chart(fig)

