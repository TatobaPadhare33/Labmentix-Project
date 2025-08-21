import streamlit as st
import pandas as pd
import numpy as np
from pandasql import sqldf
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Set page configuration
st.set_page_config(
    page_title="FMS - Food Distribution Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🍽️"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #red;
    }
    .stApp {
        background-image: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
    }
    .header-text {
        font-size: 36px !important;
        font-weight: 700 !important;
        color: #2c3e50 !important;
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        background: linear-gradient(135deg, #6dd5ed, #2193b0);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .card {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        transition: transform 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }
    .metric-card {
        background: linear-gradient(135deg, #ff512f 0%, #dd2476 100%);
        color: white;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .section-header {
        font-size: 24px !important;
        font-weight: 700 !important;
        color: #2c3e50;
        border-left: 5px solid #3498db;
        padding-left: 15px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .stSelectbox > div > div {
        border-radius: 12px !important;
    }
    .stButton>button {
        border-radius: 12px !important;
        background: linear-gradient(135deg, #00b09b, #96c93d) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        transition: all 0.3s !important;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
    }
    .insights-box {
        background-color: #e8f4f8;
        border-left: 5px solid #3498db;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data function with caching
@st.cache_data
def load_data():
    # Load datasets with error handling
    datasets = {}
    base_path = "Datasets/Cleaned-datasets/"
    
    try:
        datasets['providers'] = pd.read_csv(os.path.join(base_path, "clean_providers_data.csv"))
        datasets['receivers'] = pd.read_csv(os.path.join(base_path, "clean_receivers_data.csv"))
        datasets['food'] = pd.read_csv(os.path.join(base_path, "clean_food_listings_data.csv"))
        datasets['claims'] = pd.read_csv(os.path.join(base_path, "clean_claims_data.csv"))
        
        # Convert date columns to datetime
        if 'Expiry_Date' in datasets['food']:
            datasets['food']['Expiry_Date'] = pd.to_datetime(datasets['food']['Expiry_Date'], errors='coerce')
        
        if 'Date' in datasets['claims']:
            datasets['claims']['Date'] = pd.to_datetime(datasets['claims']['Date'], errors='coerce')
        
        return datasets
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        # Return empty dataframes if files not found
        return {
            'providers': pd.DataFrame(),
            'receivers': pd.DataFrame(),
            'food': pd.DataFrame(),
            'claims': pd.DataFrame()
        }

# Initialize data
data = load_data()
providers_df = data['providers']
receivers_df = data['receivers']
food_df = data['food']
claims_df = data['claims']

# Helper function to run SQL queries
def run_query(query):
    try:
        # Create a dictionary of available DataFrames
        tables = {
            'providers': providers_df,
            'receivers': receivers_df,
            'food': food_df,
            'claims': claims_df
        }
        # Use pandasql to execute the query
        result = sqldf(query, tables)
        return result
    except Exception as e:
        st.error(f"Query failed: {str(e)}")
        return pd.DataFrame()

# Predefined queries
predefined_queries = {
    "Total Providers": "SELECT COUNT(*) AS Total_Providers FROM providers",
    "Total Receivers": "SELECT COUNT(*) AS Total_Receivers FROM receivers",
    "Available Food Items": "SELECT COUNT(*) AS Available_Food FROM food",
    "Total Claims": "SELECT COUNT(*) AS Total_Claims FROM claims",
    "Top 10 Food Types": "SELECT Food_Type, COUNT(*) AS Count FROM food GROUP BY Food_Type ORDER BY Count DESC LIMIT 10",
    "Top 10 Providers by Food Listings": """
        SELECT p.Name, COUNT(f.Food_ID) AS Listings 
        FROM providers p 
        JOIN food f ON p.Provider_ID = f.Provider_ID 
        GROUP BY p.Name 
        ORDER BY Listings DESC 
        LIMIT 10
    """,
    "Claims by Status": "SELECT Status, COUNT(*) AS Claim_Count FROM claims GROUP BY Status",
    "Expiring Soon (Next 7 Days)": """
        SELECT * 
        FROM food 
        WHERE Expiry_Date BETWEEN date('now') AND date('now', '+7 days')
    """,
    "Top Receivers by Claims": """
        SELECT r.Name, COUNT(c.Claim_ID) AS Claims 
        FROM receivers r 
        JOIN claims c ON r.Receiver_ID = c.Receiver_ID 
        GROUP BY r.Name 
        ORDER BY Claims DESC 
        LIMIT 10
    """,
    "Food Wastage (Expired Items)": "SELECT * FROM food WHERE Expiry_Date < date('now')"
}

# Create visualizations based on EDA
def create_visualization(viz_name):
    # Provider Visualizations
    if viz_name == "Distribution of Provider Types":
        if not providers_df.empty and 'Type' in providers_df.columns:
            provider_counts = providers_df['Type'].value_counts().reset_index()
            provider_counts.columns = ['Provider_Type', 'Count']
            
            fig = px.bar(
                provider_counts, 
                x='Provider_Type', 
                y='Count',
                title='Distribution of Provider Types',
                color='Provider_Type',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(
                xaxis_title="Provider Type",
                yaxis_title="Count",
                plot_bgcolor='rgba(1,1,1,1)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            return fig
    
    elif viz_name == "Top 10 Cities by Number of Providers":
        if not providers_df.empty and 'City' in providers_df.columns:
            city_counts = providers_df['City'].value_counts().reset_index().head(10)
            city_counts.columns = ['City', 'Count']
            
            fig = px.bar(
                city_counts, 
                x='City', 
                y='Count',
                title='Top 10 Cities by Number of Providers',
                color='City',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(
                xaxis_title="City",
                yaxis_title="Number of Providers",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            return fig
    
    # Receiver Visualizations
    elif viz_name == "Distribution of Receiver Types":
        if not receivers_df.empty and 'Type' in receivers_df.columns:
            receiver_counts = receivers_df['Type'].value_counts().reset_index()
            receiver_counts.columns = ['Receiver_Type', 'Count']
            
            fig = px.pie(
                receiver_counts,
                names='Receiver_Type',
                values='Count',
                title='Distribution of Receiver Types',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            return fig
    
    # Food Visualizations
    elif viz_name == "Counts of Food Types Listed":
        if not food_df.empty and 'Food_Type' in food_df.columns:
            food_counts = food_df['Food_Type'].value_counts().reset_index()
            food_counts.columns = ['Food_Type', 'Count']
            
            fig = px.bar(
                food_counts, 
                x='Food_Type', 
                y='Count',
                title='Counts of Food Types Listed',
                color='Food_Type',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(
                xaxis_title="Food Type",
                yaxis_title="Count",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            return fig
    
    elif viz_name == "Total Quantity Donated per Food Type":
        if not food_df.empty and 'Food_Type' in food_df.columns:
            food_qty = food_df.groupby('Food_Type')['Quantity'].sum().reset_index()
            
            fig = px.bar(
                food_qty, 
                x='Food_Type', 
                y='Quantity',
                title='Total Quantity Donated per Food Type',
                color='Food_Type',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(
                xaxis_title="Food Type",
                yaxis_title="Total Quantity",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            return fig
    
    # Claims Visualizations
    elif viz_name == "Claim Status Distribution":
        if not claims_df.empty and 'Status' in claims_df.columns:
            status_counts = claims_df['Status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            
            fig = px.bar(
                status_counts, 
                x='Status', 
                y='Count',
                title='Claim Status Distribution',
                color='Status',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(
                xaxis_title="Status",
                yaxis_title="Count",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            return fig
    
    elif viz_name == "Claims Over Time":
        if not claims_df.empty and 'Timestamp' in claims_df.columns:
            try:
                claims_over_time = claims_df.copy()
                # Convert Timestamp to datetime and extract date
                claims_over_time['Date'] = pd.to_datetime(claims_over_time['Timestamp']).dt.date
                claims_over_time['Date'] = pd.to_datetime(claims_over_time['Date'])
                
                # Drop rows with invalid dates
                claims_over_time = claims_over_time.dropna(subset=['Date'])
                
                if claims_over_time.empty:
                    st.warning("No valid timestamp data available for Claims Over Time visualization.")
                    return None
                    
                # Resample by week and count claims
                claims_over_time = claims_over_time.set_index('Date').resample('W').size().reset_index()
                claims_over_time.columns = ['Date', 'Claims']
                
                # Create the line chart
                fig = px.line(
                    claims_over_time, 
                    x='Date', 
                    y='Claims',
                    title='Claims Over Time',
                    markers=True
                )
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Number of Claims",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                return fig
            except Exception as e:
                st.error(f"Error generating Claims Over Time visualization: {str(e)}")
                return None
        else:
            st.warning("Claims data is empty or Timestamp column is missing.")
            return None
    # Food Wastage Visualizations
    elif viz_name == "Food Wastage by Food Type":
        # Food wastage = expired food that wasn't claimed
        if not food_df.empty:
            # Get expired food
            expired_food = food_df.copy()
            expired_food['Expired'] = expired_food['Expiry_Date'] < datetime.now()
            
            # Merge with claims to find unclaimed food
            if not claims_df.empty:
                claimed_food_ids = claims_df['Food_ID'].unique()
                expired_food['Unclaimed'] = ~expired_food['Food_ID'].isin(claimed_food_ids)
                wastage = expired_food[(expired_food['Expired']) & (expired_food['Unclaimed'])]
                
                if not wastage.empty and 'Food_Type' in wastage.columns:
                    wastage_by_type = wastage.groupby('Food_Type')['Quantity'].sum().reset_index()
                    
                    fig = px.bar(
                        wastage_by_type, 
                        x='Food_Type', 
                        y='Quantity',
                        title='Food Wastage by Food Type',
                        color='Food_Type',
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )
                    fig.update_layout(
                        xaxis_title="Food Type",
                        yaxis_title="Wasted Quantity",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    return fig
    
    elif viz_name == "Food Wastage by Meal Type":
        # Similar to above
        if not food_df.empty:
            expired_food = food_df.copy()
            expired_food['Expired'] = expired_food['Expiry_Date'] < datetime.now()
            
            if not claims_df.empty:
                claimed_food_ids = claims_df['Food_ID'].unique()
                expired_food['Unclaimed'] = ~expired_food['Food_ID'].isin(claimed_food_ids)
                wastage = expired_food[(expired_food['Expired']) & (expired_food['Unclaimed'])]
                
                if not wastage.empty and 'Meal_Type' in wastage.columns:
                    wastage_by_meal = wastage.groupby('Meal_Type')['Quantity'].sum().reset_index()
                    
                    fig = px.pie(
                        wastage_by_meal,
                        names='Meal_Type',
                        values='Quantity',
                        title='Food Wastage by Meal Type',
                        hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    return fig
    
    # NEW VISUALIZATIONS FROM FOOD DISTRIBUTION ANALYSIS
    
    # Overall Food Claim Rate by Status
    elif viz_name == "Overall Food Claim Rate by Status":
        if not food_df.empty and not claims_df.empty:
            # Calculate the quantities for each status
            total_listed_quantity = food_df['Quantity'].sum()
            
            # Get completed claims
            completed_claims_df = claims_df[claims_df['Status'] == 'Completed']
            completed_food_ids = completed_claims_df['Food_ID'].unique()
            completed_food_df = food_df[food_df['Food_ID'].isin(completed_food_ids)]
            completed_claims_quantity = completed_food_df['Quantity'].sum()
            
            # Get cancelled claims
            cancelled_claims_df = claims_df[claims_df['Status'] == 'Cancelled']
            cancelled_food_ids = cancelled_claims_df['Food_ID'].unique()
            cancelled_food_df = food_df[food_df['Food_ID'].isin(cancelled_food_ids)]
            cancelled_claims_quantity = cancelled_food_df['Quantity'].sum()
            
            # Get pending claims
            pending_claims_df = claims_df[claims_df['Status'] == 'Pending']
            pending_food_ids = pending_claims_df['Food_ID'].unique()
            pending_food_df = food_df[food_df['Food_ID'].isin(pending_food_ids)]
            pending_claims_quantity = pending_food_df['Quantity'].sum()
            
            # Calculate unclaimed quantity
            unclaimed_quantity = total_listed_quantity - (completed_claims_quantity + cancelled_claims_quantity + pending_claims_quantity)
            
            # Calculate percentages
            percentage_completed = (completed_claims_quantity / total_listed_quantity) * 100 if total_listed_quantity > 0 else 0
            percentage_cancelled = (cancelled_claims_quantity / total_listed_quantity) * 100 if total_listed_quantity > 0 else 0
            percentage_pending = (pending_claims_quantity / total_listed_quantity) * 100 if total_listed_quantity > 0 else 0
            percentage_unclaimed = (unclaimed_quantity / total_listed_quantity) * 100 if total_listed_quantity > 0 else 0
            
            # Create a DataFrame for plotting
            claim_status_data = pd.DataFrame({
                'Status': ['Completed', 'Cancelled', 'Pending', 'Unclaimed'],
                'Percentage': [percentage_completed, percentage_cancelled, percentage_pending, percentage_unclaimed]
            })
            
            fig = px.bar(
                claim_status_data,
                x='Status',
                y='Percentage',
                title='Overall Food Claim Rate by Status',
                color='Status',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(
                xaxis_title="Claim Status",
                yaxis_title="Percentage of Total Listed Quantity",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            return fig
    
    # Listed vs. Claimed Quantity for Top 10 Locations by Claim Rate
    elif viz_name == "Listed vs. Claimed Quantity for Top 10 Locations by Claim Rate":
        if not food_df.empty and not claims_df.empty:
            # Merge the food_df and claims_df DataFrames
            merged_df = pd.merge(food_df, claims_df, on='Food_ID', how='left')
            
            # Calculate listed quantity by location
            listed_quantity_by_location = food_df.groupby('Location')['Quantity'].sum().reset_index()
            listed_quantity_by_location.rename(columns={'Quantity': 'Listed_Quantity'}, inplace=True)
            
            # Calculate claimed quantity by location
            completed_claims_df = merged_df[merged_df['Status'] == 'Completed'].copy()
            claimed_quantity_by_location = completed_claims_df.groupby('Location')['Quantity'].sum().reset_index()
            claimed_quantity_by_location.rename(columns={'Quantity': 'Claimed_Quantity'}, inplace=True)
            
            # Merge the listed and claimed quantities by location
            location_claim_rates = pd.merge(listed_quantity_by_location, claimed_quantity_by_location, on='Location', how='left')
            location_claim_rates['Claimed_Quantity'] = location_claim_rates['Claimed_Quantity'].fillna(0)
            
            # Calculate the claim rate for each location
            location_claim_rates['Claim_Rate'] = (location_claim_rates['Claimed_Quantity'] / location_claim_rates['Listed_Quantity']) * 100
            
            # Get top 10 locations by claim rate
            top_10_locations = location_claim_rates.sort_values(by='Claim_Rate', ascending=False).head(10)
            
            # Melt the DataFrame for plotting
            top_10_melted = top_10_locations.melt(
                id_vars='Location', 
                value_vars=['Listed_Quantity', 'Claimed_Quantity'],
                var_name='Quantity_Type', 
                value_name='Quantity'
            )
            
            fig = px.bar(
                top_10_melted,
                x='Location',
                y='Quantity',
                color='Quantity_Type',
                title='Listed vs. Claimed Quantity for Top 10 Locations by Claim Rate',
                barmode='group',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(
                xaxis_title="Location",
                yaxis_title="Quantity",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            return fig
    
    # Listed vs. Claimed Quantity for Bottom 10 Locations by Claim Rate
    elif viz_name == "Listed vs. Claimed Quantity for Bottom 10 Locations by Claim Rate":
        if not food_df.empty and not claims_df.empty:
            # Merge the food_df and claims_df DataFrames
            merged_df = pd.merge(food_df, claims_df, on='Food_ID', how='left')
            
            # Calculate listed quantity by location
            listed_quantity_by_location = food_df.groupby('Location')['Quantity'].sum().reset_index()
            listed_quantity_by_location.rename(columns={'Quantity': 'Listed_Quantity'}, inplace=True)
            
            # Calculate claimed quantity by location
            completed_claims_df = merged_df[merged_df['Status'] == 'Completed'].copy()
            claimed_quantity_by_location = completed_claims_df.groupby('Location')['Quantity'].sum().reset_index()
            claimed_quantity_by_location.rename(columns={'Quantity': 'Claimed_Quantity'}, inplace=True)
            
            # Merge the listed and claimed quantities by location
            location_claim_rates = pd.merge(listed_quantity_by_location, claimed_quantity_by_location, on='Location', how='left')
            location_claim_rates['Claimed_Quantity'] = location_claim_rates['Claimed_Quantity'].fillna(0)
            
            # Calculate the claim rate for each location
            location_claim_rates['Claim_Rate'] = (location_claim_rates['Claimed_Quantity'] / location_claim_rates['Listed_Quantity']) * 100
            
            # Get bottom 10 locations by claim rate
            bottom_10_locations = location_claim_rates.sort_values(by='Claim_Rate', ascending=True).head(10)
            
            # Melt the DataFrame for plotting
            bottom_10_melted = bottom_10_locations.melt(
                id_vars='Location', 
                value_vars=['Listed_Quantity', 'Claimed_Quantity'],
                var_name='Quantity_Type', 
                value_name='Quantity'
            )
            
            fig = px.bar(
                bottom_10_melted,
                x='Location',
                y='Quantity',
                color='Quantity_Type',
                title='Listed vs. Claimed Quantity for Bottom 10 Locations by Claim Rate',
                barmode='group',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(
                xaxis_title="Location",
                yaxis_title="Quantity",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            return fig
    
    # Claimed Quantity by Food Type
    elif viz_name == "Claimed Quantity by Food Type":
        if not claims_df.empty and not food_df.empty:
            # Merge claims and food
            merged = pd.merge(claims_df, food_df, on='Food_ID', how='left')
            if 'Food_Type' in merged.columns:
                food_claims = merged[merged['Status'] == 'Completed'].groupby('Food_Type')['Quantity'].sum().reset_index()
                
                fig = px.bar(
                    food_claims, 
                    x='Food_Type', 
                    y='Quantity',
                    title='Claimed Quantity by Food Type',
                    color='Food_Type',
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig.update_layout(
                    xaxis_title="Food Type",
                    yaxis_title="Claimed Quantity",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                return fig
    
    # Claimed Quantity by Meal Type
    elif viz_name == "Claimed Quantity by Meal Type":
        if not claims_df.empty and not food_df.empty:
            # Merge claims and food
            merged = pd.merge(claims_df, food_df, on='Food_ID', how='left')
            if 'Meal_Type' in merged.columns:
                meal_claims = merged[merged['Status'] == 'Completed'].groupby('Meal_Type')['Quantity'].sum().reset_index()
                
                fig = px.pie(
                    meal_claims,
                    names='Meal_Type',
                    values='Quantity',
                    title='Claimed Quantity by Meal Type',
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                return fig
    
    # Top 10 Providers by Donated Quantity
    elif viz_name == "Top 10 Providers by Donated Quantity":
        if not food_df.empty and not providers_df.empty:
            # Merge food and providers
            merged = pd.merge(food_df, providers_df, on='Provider_ID', how='left')
            provider_qty = merged.groupby('Name')['Quantity'].sum().reset_index()
            provider_qty = provider_qty.sort_values('Quantity', ascending=False).head(10)
            
            fig = px.bar(
                provider_qty, 
                x='Name', 
                y='Quantity',
                title='Top 10 Providers by Donated Quantity',
                color='Name',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(
                xaxis_title="Provider",
                yaxis_title="Total Quantity Donated",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            return fig
    
    # Top 10 Receivers by Claim Count
    elif viz_name == "Top 10 Receivers by Claim Count":
        if not claims_df.empty and not receivers_df.empty:
            # Merge claims and receivers
            merged = pd.merge(claims_df, receivers_df, on='Receiver_ID', how='left')
            receiver_claims = merged[merged['Status'] == 'Completed'].groupby('Name').size().reset_index()
            receiver_claims.columns = ['Receiver_Name', 'Claim_Count']
            receiver_claims = receiver_claims.sort_values('Claim_Count', ascending=False).head(10)
            
            fig = px.bar(
                receiver_claims, 
                x='Receiver_Name', 
                y='Claim_Count',
                title='Top 10 Receivers by Claim Count',
                color='Receiver_Name',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(
                xaxis_title="Receiver",
                yaxis_title="Number of Claims",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            return fig
    
    # If visualization not found, return None
    return None

# Main App
def main():
    # Header
    st.markdown('<div class="header-text">🍽️ Local Food Wastage Management System Dashboard</div>', unsafe_allow_html=True)
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card">'
                    '<h3>Total Providers</h3>'
                    f'<h1>{len(providers_df) if not providers_df.empty else 0}</h1>'
                    '</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">'
                    '<h3>Total Receivers</h3>'
                    f'<h1>{len(receivers_df) if not receivers_df.empty else 0}</h1>'
                    '</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">'
                    '<h3>Food Listings</h3>'
                    f'<h1>{len(food_df) if not food_df.empty else 0}</h1>'
                    '</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card">'
                    '<h3>Total Claims</h3>'
                    f'<h1>{len(claims_df) if not claims_df.empty else 0}</h1>'
                    '</div>', unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["SQL Queries", "Data Visualizations", "Data Explorer"])
    
    with tab1:
        st.markdown('<div class="section-header">SQL Query Interface</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("### Predefined Queries")
            selected_query = st.selectbox("Select a query:", list(predefined_queries.keys()))
            
            if st.button("Run Selected Query"):
                query = predefined_queries[selected_query]
                st.session_state.current_query = query
                st.session_state.query_result = run_query(query)
        
        with col2:
            st.markdown("### Custom Query")
            custom_query = st.text_area("Enter your SQL query:", height=200,
                                      value=st.session_state.get('current_query', 'SELECT * FROM food LIMIT 10'))
            
            if st.button("Run Custom Query"):
                st.session_state.current_query = custom_query
                st.session_state.query_result = run_query(custom_query)
        
        if 'query_result' in st.session_state and not st.session_state.query_result.empty:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Query Results")
            st.dataframe(st.session_state.query_result, use_container_width=True)
            st.markdown(f"**Rows returned:** {len(st.session_state.query_result)}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="section-header">Data Visualizations</div>', unsafe_allow_html=True)
        
        # Add key insights section
        st.markdown('<div class="insights-box">', unsafe_allow_html=True)
        st.markdown("### Key Insights from Food Distribution Analysis")
        st.markdown("""
        - **Overall Food Claim Rate**: 28.36% of listed food is successfully claimed, with 7314 units claimed out of 25794 units listed.
        - **Location Disparities**: Claim rates vary significantly by location, with some locations having claim rates over 100% (potentially indicating data issues) and others having 0% claim rates.
        - **Food Type Preferences**: 'Non-Vegetarian' food is the most claimed food type (3125 units), while 'Vegan' is the least claimed (2565 units).
        - **Meal Type Preferences**: 'Breakfast' is the most claimed meal type (2423 units), and 'Snacks' are the least claimed (2043 units).
        - **Top Provider**: 'Barry Group' is the top provider by donated quantity (179 units).
        - **Top Receivers**: 'William Frederick', 'Anthony Garcia', and 'Matthew Webb' are the top receivers by claim count (5 claims each).
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Group visualizations by category
        viz_categories = {
            "Overview": [
                "Overall Food Claim Rate by Status"
            ],
            "Providers": [
                "Distribution of Provider Types",
                "Top 10 Cities by Number of Providers",
                "Top 10 Providers by Donated Quantity"
            ],
            "Receivers": [
                "Distribution of Receiver Types",
                "Top 10 Receivers by Claim Count"
            ],
            "Food": [
                "Counts of Food Types Listed",
                "Total Quantity Donated per Food Type",
                "Claimed Quantity by Food Type",
                "Claimed Quantity by Meal Type"
            ],
            "Location Analysis": [
                "Listed vs. Claimed Quantity for Top 10 Locations by Claim Rate",
                "Listed vs. Claimed Quantity for Bottom 10 Locations by Claim Rate"
            ],
            "Claims": [
                "Claim Status Distribution",
                "Claims Over Time"
            ],
            "Food Wastage": [
                "Food Wastage by Food Type",
                "Food Wastage by Meal Type"
            ]
        }
        
        # Visualization selector
        selected_category = st.selectbox("Select Visualization Category:", list(viz_categories.keys()))
        selected_viz = st.selectbox("Select Visualization:", viz_categories[selected_category])
        
        # Create and display visualization
        if st.button("Generate Visualization"):
            fig = create_visualization(selected_viz)
            if fig:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("Could not generate visualization. Check if required data is available.")
    
    with tab3:
        st.markdown('<div class="section-header">Data Explorer</div>', unsafe_allow_html=True)
        
        dataset = st.selectbox("Select Dataset:", ["Providers", "Receivers", "Food Listings", "Claims"])
        
        if dataset == "Providers" and not providers_df.empty:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.dataframe(providers_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        elif dataset == "Receivers" and not receivers_df.empty:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.dataframe(receivers_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        elif dataset == "Food Listings" and not food_df.empty:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.dataframe(food_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        elif dataset == "Claims" and not claims_df.empty:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.dataframe(claims_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Selected dataset is empty or not available.")

# Run the app
if __name__ == "__main__":
    main()