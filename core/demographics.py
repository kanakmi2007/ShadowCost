"""
core/demographics.py - Synthetic Urban Fabric Spatial Layer Generator
"""

import numpy as np
import streamlit as st
import geopandas as gpd
from shapely.geometry import Polygon


@st.cache_data(show_spinner=False)
def generate_demographic_features(center_lat: float, center_lon: float, seed: int = 42) -> gpd.GeoDataFrame:
    """
    Generates a deterministic synthetic urban spatial dataset around the center point.
    Contains parks, commercial centers, residential apartments, and civic structures.
    """
    rng = np.random.default_rng(seed)
    features = []
    d_lat, d_lon = 0.009, 0.010

    def add_rect(name, category, lat, lon, w_lat, w_lon, building=None, shop=None, amenity=None,
                 density=0, footfall=0, green=False):
        poly = Polygon([
            (lon - w_lon / 2, lat - w_lat / 2),
            (lon + w_lon / 2, lat - w_lat / 2),
            (lon + w_lon / 2, lat + w_lat / 2),
            (lon - w_lon / 2, lat + w_lat / 2),
            (lon - w_lon / 2, lat - w_lat / 2)
        ])
        features.append({
            "osmid": f"{category}_{len(features) + 1}",
            "name": name,
            "building": building,
            "leisure": "park" if category == "park" else None,
            "shop": shop,
            "amenity": amenity,
            "category": category,
            "density_multiplier": density,
            "footfall_multiplier": footfall,
            "green_cover": green,
            "geometry": poly
        })

    # 1. Eco Canopies & Parks (7 features)
    for i in range(7):
        add_rect(
            f"Community Park & Eco Canopy #{i + 1}", "park",
            center_lat + rng.uniform(-d_lat * .85, d_lat * .85),
            center_lon + rng.uniform(-d_lon * .85, d_lon * .85),
            rng.uniform(.0016, .0032), rng.uniform(.002, .004),
            footfall=80, green=True
        )

    # 2. Commercial Retail & Malls (12 features)
    for i in range(12):
        mall = (i % 3 == 0)
        add_rect(
            f"Shopping Mall & Complex #{i + 1}" if mall else f"Commercial Retail Arcade #{i + 1}", "commercial",
            center_lat + rng.uniform(-d_lat * .88, d_lat * .88),
            center_lon + rng.uniform(-d_lon * .88, d_lon * .88),
            rng.uniform(.0009, .0017), rng.uniform(.0011, .0022),
            building="mall" if mall else "retail",
            shop="mall" if mall else "supermarket",
            amenity="marketplace" if mall else "restaurant",
            density=20, footfall=2400 if mall else 750
        )

    # 3. Residential Blocks & Apartments (22 features)
    for i in range(22):
        apt = (i % 2 == 0)
        add_rect(
            f"Multi-Story Apartment Complex #{i + 1}" if apt else f"Residential Housing Block #{i + 1}", "residential",
            center_lat + rng.uniform(-d_lat * .90, d_lat * .90),
            center_lon + rng.uniform(-d_lon * .90, d_lon * .90),
            rng.uniform(.0007, .0014), rng.uniform(.0009, .0018),
            building="apartments" if apt else "residential",
            density=180 if apt else 45, footfall=140
        )

    # 4. Civic & Mixed-Use Facilities (15 features)
    for i in range(15):
        add_rect(
            f"Civic & Mixed-Use Structure #{i + 1}", "other",
            center_lat + rng.uniform(-d_lat * .85, d_lat * .85),
            center_lon + rng.uniform(-d_lon * .85, d_lon * .85),
            rng.uniform(.0006, .0011), rng.uniform(.0007, .0013),
            building="yes",
            amenity="school" if i % 2 == 0 else "health_centre",
            density=30, footfall=320
        )

    return gpd.GeoDataFrame(features, crs="EPSG:4326")
