import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# --- Page Configuration (must be the first Streamlit command) ---
st.set_page_config(
    page_title="Odisha Traffic Dashboard",
    page_icon="🚦",
    layout="wide"
)

# --- Custom CSS for a Dark Theme and Better Fonts ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Create a style.css file with the CSS content below, or just run this.
# For simplicity, we'll inject the CSS directly.
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1a1a2e;
    }
    /* Font styling */
    h1, h2, h3 {
        font-family: 'Helvetica', 'Arial', sans-serif;
    }
    .stMetric {
        border: 1px solid #262730;
        border-radius: 10px;
        padding: 15px;
        background-color: #1E2128;
    }
</style>
""", unsafe_allow_html=True)


# --- 1. LOAD YOUR ACTUAL DATA ---
@st.cache_data
def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df['Hour'] = df['DateTime'].dt.hour
        return df
    except FileNotFoundError:
        st.error(f"Error: The file '{filepath}' was not found.")
        return None

# Load your data
heatmap_df = load_data("heatmap_data_inspired_odisha.csv")


# --- 2. SETUP SIDEBAR ---
st.sidebar.header("Dashboard Controls")
hour_to_filter = st.sidebar.slider('Hour of Day', 0, 23, 8)


# --- 3. MAIN PANEL ---
st.title("🚦 Odisha Live Traffic Dashboard")
st.write(f"Displaying traffic congestion for **{hour_to_filter}:00**")

if heatmap_df is not None:
    filtered_data = heatmap_df[heatmap_df['Hour'] == hour_to_filter]
    
    # --- Display Key Metrics ---
    total_vehicles = filtered_data['Vehicles'].sum()
    active_junctions = len(filtered_data)
    
    col1, col2 = st.columns(2)
    col1.metric("Total Vehicles (Selected Hour)", f"{total_vehicles:,}")
    col2.metric("Active Junctions", f"{active_junctions}")

    st.markdown("---")
 # --- 4. CREATE THE MAP (with tighter boundaries) ---
    # Define a tighter bounding box for Odisha
    odisha_bounds = [
        [18.1, 82.0],  # Southwest corner [min_lat, min_lon]
        [22.4, 87.2]   # Northeast corner [max_lat, max_lon]
    ]
    map_center = [20.9517, 85.0985]

    # Create the map with the new, tighter max_bounds
    m = folium.Map(
        location=map_center, 
        zoom_start=8, # Increased initial zoom level
        max_bounds=True,
        min_lat=odisha_bounds[0][0],
        max_lat=odisha_bounds[1][0],
        min_lon=odisha_bounds[0][1],
        max_lon=odisha_bounds[1][1],
        min_zoom=8 # Increased min_zoom to prevent zooming out too far
    )

    heat_data = filtered_data[['Latitude', 'Longitude', 'Vehicles']].values.tolist()

    if heat_data:
        HeatMap(heat_data, radius=15, blur=20).add_to(m)
    else:
        st.warning(f"No traffic data available for hour {hour_to_filter}:00.")

    # --- 5. DISPLAY THE MAP ---
    st_folium(m, width=1200, height=500, use_container_width=True)