import streamlit as st
import time
import ast
from streamlit_folium import folium_static
import folium
from folium.plugins import Search

st.set_page_config(layout="wide")

st.markdown("""
<style>
    .traffic-light-container {
        background-color: #000000;
        padding: 10px;
        border-radius: 10px;
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
        border: 2px solid #333;
    }
    .traffic-light-circle {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background-color: #374151;
        box-shadow: inset 2px 2px 4px rgba(0,0,0,0.5);
        transition: all 0.3s ease;
    }
    .glow-red { background-color: #ef4444; box-shadow: 0 0 15px 5px #ef4444; }
    .glow-yellow { background-color: #f59e0b; box-shadow: 0 0 15px 5px #f59e0b; }
    .glow-green { background-color: #22c55e; box-shadow: 0 0 15px 5px #22c55e; }
</style>
""", unsafe_allow_html=True)

st.title("Traffic Congestion Management System")

with st.sidebar:
    st.header("Controls")
    view_mode = st.radio("Select View", ("Traffic", "Heatmap"))

if 'lanes' not in st.session_state:
    st.session_state.lanes = {
        "L1": "red",
        "L2": "red",
        "L3": "red",
        "L4": "red",
    }

def display_traffic_light(current_color):
    colors = ["red", "yellow", "green"]
    html_circles = ""
    for color in colors:
        glow_class = f"glow-{color}" if current_color == color else ""
        html_circles += f'<div class="traffic-light-circle {glow_class}"></div>'
    st.markdown(f'<div class="traffic-light-container">{html_circles}</div>', unsafe_allow_html=True)

def read_traffic_data(filepath="traffic_data.txt"):
    try:
        with open(filepath, 'r') as f:
            data_str = f.read()
            return ast.literal_eval(data_str)
    except FileNotFoundError:
        st.error(f"Error: The data file '{filepath}' was not found.")
        st.info(f"Please create '{filepath}' in the same directory as the app.")
        return None
    except Exception as e:
        st.error(f"Error parsing the data file: {e}")
        return None

# --- Render different views in placeholders so map doesn't persist ---
traffic_placeholder = st.empty()
heatmap_placeholder = st.empty()

if view_mode == "Traffic":
    with traffic_placeholder.container():
        traffic_data = read_traffic_data()
        if traffic_data:
            for lane, is_green in traffic_data.items():
                if lane in st.session_state.lanes:
                    st.session_state.lanes[lane] = "green" if is_green else "red"
        lanes = list(st.session_state.lanes.keys())
        cols = st.columns(len(lanes))
        for i, lane_name in enumerate(lanes):
            with cols[i]:
                st.header(lane_name)
                display_traffic_light(st.session_state.lanes[lane_name])
                st.write("")
        time.sleep(1)
        st.rerun()

elif view_mode == "Heatmap":
    with heatmap_placeholder.container():
        m = folium.Map(location=[20.2961, 85.8245], zoom_start=13, tiles="OpenStreetMap")
        locations = {
            "KIIT University": [20.2961, 85.8245],
            "Bhubaneswar Railway Station": [20.2686, 85.8436],
            "Nandankanan Zoo": [20.3965, 85.8175]
        }
        for name, coords in locations.items():
            folium.Marker(coords, popup=name, tooltip=name).add_to(m)
        fg = folium.FeatureGroup(name="Searchable Locations").add_to(m)
        for name, coords in locations.items():
            folium.Marker(coords, popup=name, tooltip=name).add_to(fg)
        Search(
            layer=fg,
            search_label="name",
            placeholder="Search for a place...",
            collapsed=False
        ).add_to(m)
        st.header("Traffic Congestion Heatmap")
        st.write("The map below shows a heatmap of traffic congestion with search functionality.")
        folium_static(m)
