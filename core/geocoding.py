"""
core/geocoding.py - Location Resolver & Spatial Buffer Engine
"""

import streamlit as st
import geopandas as gpd
import osmnx as ox
from shapely.geometry import Point
from config import KNOWN_CITIES


def safe_geocode(city_query: str):
    """Return (lat, lon, display_name) or None. Never silently substitute another city."""
    if not city_query or not city_query.strip():
        return None
        
    clean = city_query.strip().lower()
    if clean in KNOWN_CITIES:
        return KNOWN_CITIES[clean]
        
    try:
        lat, lon = ox.geocode(city_query.strip())
        return float(lat), float(lon), f"{city_query.strip()} (geocoded)"
    except Exception:
        try:
            gdf = ox.geocode_to_gdf(city_query.strip())
            if len(gdf):
                return float(gdf.lat.iloc[0]), float(gdf.lon.iloc[0]), str(gdf.display_name.iloc[0])
        except Exception:
            pass
    return None


@st.cache_data(show_spinner=False)
def geocode_city_with_buffer(city_query: str, buffer_meters: float = 2000.0):
    """
    Geocodes city and returns (lat, lon, buffer_polygon_4326, bounds, display_name).
    """
    result = safe_geocode(city_query)
    if result is None:
        return None
        
    center_lat, center_lon, display_name = result
    pt = Point(center_lon, center_lat)
    pt_gdf = gpd.GeoDataFrame([{"geometry": pt}], crs="EPSG:4326")
    
    try:
        utm_crs = pt_gdf.estimate_utm_crs()
        buf_utm = pt_gdf.to_crs(utm_crs).buffer(buffer_meters)
        buf_4326 = buf_utm.to_crs("EPSG:4326").iloc[0]
    except Exception:
        d_deg = buffer_meters / 111320.0
        buf_4326 = pt.buffer(d_deg)
        
    min_lon, min_lat, max_lon, max_lat = buf_4326.bounds
    return center_lat, center_lon, buf_4326, (min_lon, min_lat, max_lon, max_lat), display_name
