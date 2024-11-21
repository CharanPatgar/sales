import pandas as pd
import streamlit as st
import plotly.express as px

# Set Streamlit layout to wide mode
st.set_page_config(layout="wide")

# Load data
sales_data = pd.read_csv("Sales Data.csv")
product_data = pd.read_csv("Product Data.csv")
customer_data = pd.read_csv("Customer Data.csv")
region_data = pd.read_csv("Region Data.csv")

# Step 2: Merge Data
merged_data = sales_data.merge(customer_data, left_on="Sales ID", right_on="Customer ID", how="left")
merged_data["Region"] = sales_data["Region"]
merged_data = merged_data.merge(product_data, on="Product ID", how="left")
if "Region" in merged_data.columns:
    merged_data = merged_data.merge(region_data, on="Region", how="left")
else:
    st.error("The Region column is missing in the merged data!")

# Define Tabs
tabs = st.tabs(["Dashboard", "Regional Insights", "Product Insights", "Customer Insights", "Quarterly Insights","Overall Summary"])

# Dashboard Tab
with tabs[0]:
    st.title("Sales Dashboard")

    # Sidebar Filters
    st.sidebar.header("Filters")
    selected_region = st.sidebar.multiselect("Select Region", merged_data["Region"].unique(), default=list(merged_data["Region"].unique()))
    selected_product = st.sidebar.multiselect("Select Product Category", merged_data["Product Category"].unique(), default=list(merged_data["Product Category"].unique()))
    selected_gender = st.sidebar.multiselect("Select Gender", merged_data["Gender"].unique(), default=list(merged_data["Gender"].unique()))

    # Handle case when no filters are selected
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

    # Regional Sales
    region_sales = filtered_data.groupby("Region")["Sales Amount"].sum().reset_index()
    fig1 = px.bar(region_sales, x="Region", y="Sales Amount", 
                  title="Total Sales by Region", 
                  labels={"Sales Amount": "Sales Amount", "Region": "Region"},
                  hover_data=["Sales Amount"], color="Region", 
                  color_discrete_sequence=px.colors.qualitative.Set2)
    
    # Product Category Sales
    category_sales = filtered_data.groupby("Product Category")["Sales Amount"].sum().reset_index()
    fig2 = px.pie(category_sales, names="Product Category", values="Sales Amount", 
                  title="Sales Distribution by Product Category",
                  color="Product Category", 
                  color_discrete_sequence=px.colors.qualitative.Set3)
    fig2.update_traces(hovertemplate="Product category: %{label}<br>Sales Amount: %{value}")

    # Customer Demographics
    fig3 = px.scatter(filtered_data, x="Age", y="Sales Amount", 
                      title="Customer Age vs Sales Amount", 
                      labels={"Age": "Customer Age", "Sales Amount": "Total Sales Amount"},
                      color="Gender",  # Color points by Gender
                      color_discrete_map={"Male": "blue", "Female": "red"},  # Set custom colors for Male and Female
                      hover_data=["Age", "Sales Amount"])

    # Quarterly Sales
    merged_data["Sales Date"] = pd.to_datetime(merged_data["Sales Date"], errors='coerce')
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
            return "Out of Range"

    merged_data["Quarter"] = merged_data["Sales Date"].apply(assign_quarter)
    quarterly_sales = merged_data.groupby("Quarter")["Sales Amount"].sum().reset_index()
    fig4 = px.line(quarterly_sales, x="Quarter", y="Sales Amount", 
                   title="Quarterly Sales Trend", 
                   labels={"Quarter": "Quarter", "Sales Amount": "Total Sales Amount"},
                   markers=True, line_shape="linear")

    # Display Charts with "Show Insights" Buttons
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)


    with col2:
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(fig3, use_container_width=True)


    with col4:
        st.plotly_chart(fig4, use_container_width=True)

# Insights Tabs
with tabs[1]:
    st.header("Regional Insights")
    st.subheader("Key Findings:")
    st.write("""    

    - Highest Sales Region: The region with the highest sales is South. This indicates strong market potential in this area and highlights it as a key region to focus on.
    - Lowest Sales Region: The region with the lowest sales is East. This could indicate a need for improved marketing or a better understanding of customer preferences in this region.
    - Balanced Distribution: Sales are moderately distributed across other regions, with South and West performing consistently.
    """)
    st.subheader("Sales Distribution:")
    st.write("""
                - North Region: $1,800 (22.5%)                
                - South Region: $2,200 (27.5%)                
                - East Region: $1,600 (20%)                
                - West Region: $2,000 (25%)
            """)

with tabs[2]:
    st.header("Product Insights")
    st.subheader("Key Findings:")
    st.write("""    

    - Top-Performing Product Category: The Electronics category contributes the most to sales, showing high customer demand for these products.
    - Slightly Underperforming Category: The Fashion category has comparatively lower sales, possibly due to competition or lack of product variety.
    - Customer Preferences: Electronics outperform other categories, highlighting strong consumer interest in tech and gadgets.
    """)
    st.subheader("Sales by Product Category")
    st.write(""" 
                - Electronics (TV, Laptop): $4,200 (55.3%)
                - Fashion (Shirt, Dress): $3,400 (44.7%)
             """)

with tabs[3]:
    st.header("Customer Insights")
    st.subheader("Key Findings:")
    st.write("""

    - Age Groups with Highest Spending: Customers aged 20-35 contribute the most to sales. This is a prime demographic to target with personalized marketing campaigns.
    - Gender Distribution: Male and female customers show balanced contributions to sales, but males slightly outspend females in electronics.
    - Customer Demographics and Behavior: Younger customers (20-25) show increasing purchasing activity, while older demographics (40+) contribute less.
    """)
    st.write("""
                - Age Range: 20-40 years
                
             """)

with tabs[4]:
    st.header("Quarterly Insights")
    st.subheader("Key Findings:")
    st.write("""    

    - Highest Sales Quarter: The Last quarter (Q4) has the highest sales, followed by the First Quarterv(Q1), likely due to end/start of the month.
    - Steady Decline: Sales show a slight decline from Q2 to Q3, indicating reduced customer activity or seasonal effects.
    - Quarterly Trends: The sales trend suggests a strong start to the Month, followed by consistent but lower performance in subsequent quarters, and the go high for the last one.
    """)
    st.subheader("Quarterly sales :")
    st.write("""
             - Q1: $1800
             - Q2: $2200
             - Q3: $900
             - Q4: $2700
             """)
with tabs[5]:
    st.header("Overall Summary and Strategies")
    st.subheader("Summary :")
    
    st.subheader("1. Key Growth Areas:")
    st.write("""
              - South region and Electronics category show the most promise for growth, while the East region and Fashion category require attention.
              - The Electronics had more sales revenue than the Fashion.
             """)
    
    st.subheader("2. Customer Strategy:")
    st.write("""
             - Focus on connecting with customers aged 25-35 through personalized marketing campaigns, as they are the biggest contributors to sales. Also, keep an eye on younger customers (20-25), whose buying activity is steadily increasing, and create strategies to attract and engage them further.
             """)
    
    st.subheader("3. Quarterly analysis")
    st.write("""
             - Sales are strongest in Q1, driven by high customer demand early in the year(month), likely influenced by seasonal factors and the start of new purchasing cycles. However, sales gradually decline across Q2 to Q4, reflecting a steady but lower performance in later months. This highlights the importance of early-year activity in shaping overall sales trends.

             """)
    
    
    st.subheader("Strategies :")
    st.subheader("1. Enhance Regional Strategies:")
    st.write("""
        
        - Focus on regions like North, where sales are highest, by investing in marketing campaigns and expanding product availability to maintain the lead.
        - Conduct market research in underperforming regions like East to identify barriers and opportunities. 
        - For instance, introduce promotional discounts or localized marketing to attract customers.
    """)
    st.subheader("2. Prioritize High-Performing Product Categories:")
    st.write("""            

                - Scale up the Electronics category by ensuring sufficient stock levels, launching new products, and promoting bundled offers.
                - Address challenges in the Fashion category by understanding customer preferences, offering seasonal promotions, and improving variety or pricing.
             """)
    st.subheader("3. Leverage Customer Demographics:")
    st.write("""             

                - Target the 25-35 age group, the highest spending demographic, with personalized marketing campaigns, loyalty rewards, and product recommendations.
                - Develop strategies to engage younger customers (20-25) by leveraging digital channels like social media and gamified shopping experiences.
                - Tailor messaging for older customers (40+) with a focus on simplicity, value-for-money, and practical product options.
             """)
    st.subheader("4. Optimize Quarterly Sales Performance:")
    st.write("""             

                - Prepare for Q1, the strongest quarter, by ramping up inventory, launching holiday-specific promotions, and leveraging the seasonal buying trend.
                - Introduce mid-year and end-of-year campaigns to stimulate demand during Q2 and Q4, such as flash sales or promotions or exclusive product launches.
             """)
    st.subheader("5. Other Strategies: ")
    st.write("""
                - Tailor region-specific campaigns based on performance. For example, offer free shipping or next-day delivery in regions with high potential but low sales, like East.
                - Invest in partnerships with local influencers or events to increase brand visibility in underperforming regions.
                - Encourage repeat purchases by offering subscription-based services or loyalty programs for frequently purchased items.
             """)
