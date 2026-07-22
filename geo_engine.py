import folium
from folium.plugins import HeatMap, MarkerCluster
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

def generate_hotspot_map(filter_type="All"):
    # 1. Synthetic Data: Real coordinates for Indian Scam Hubs
    # In a real app, this would come from your SQL/NoSQL database
    data = [
        {"lat": 28.4595, "lon": 77.0266, "city": "Gurgaon", "type": "Digital Arrest", "count": 45, "intensity": 0.9},
        {"lat": 23.6102, "lon": 86.4331, "city": "Dhanbad", "type": "Phishing Hub", "count": 80, "intensity": 1.0},
        {"lat": 19.0760, "lon": 72.8777, "city": "Mumbai", "type": "Mule Account Activity", "count": 30, "intensity": 0.6},
        {"lat": 28.7041, "lon": 77.1025, "city": "Delhi", "type": "Digital Arrest", "count": 65, "intensity": 0.8},
        {"lat": 12.9716, "lon": 77.5946, "city": "Bangalore", "type": "Tech Support Scam", "count": 25, "intensity": 0.5},
        {"lat": 24.2170, "lon": 86.6500, "city": "Jamtara", "type": "KYC Scam", "count": 120, "intensity": 1.0},
    ]
    df = pd.DataFrame(data)

    # Filter data based on UI selection
    if filter_type != "All":
        df = df[df['type'] == filter_type]

    # 2. Initialize Map (Centered on India)
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles="CartoDB DarkMatter")

    # 3. Add HeatMap Layer (Shows Density)
    heat_data = [[row['lat'], row['lon'], row['intensity']] for index, row in df.iterrows()]
    HeatMap(heat_data, radius=15, blur=10, gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}).add_to(m)

    # 4. Add Marker Clusters (Click to see details)
    marker_cluster = MarkerCluster().add_to(m)
    for index, row in df.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f"<b>City:</b> {row['city']}<br><b>Primary Threat:</b> {row['type']}<br><b>Reports:</b> {row['count']}",
            icon=folium.Icon(color="red" if row['intensity'] > 0.7 else "orange", icon="info-sign")
        ).add_to(marker_cluster)

    return m