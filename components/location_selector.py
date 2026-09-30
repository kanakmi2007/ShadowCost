"""
components/location_selector.py - Location & Spatial Bounds Selection Stage (Developer Theme)
Flagship Location Stage for ShadowCost
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
from config import KNOWN_CITIES, SVG_ICONS, OSM_TILES, OSM_ATTR, DARK_TILE_CSS
from core.geocoding import geocode_city_with_buffer


def render_location_stage(on_next_callback=None):
    """Renders Location Selection Screen with Step Drawer, Presets, and Keyless OSM Dark Preview."""

    # STEP PROGRESS DRAWER
    st.markdown(
        f"""
        <div class="step-drawer">
            <div class="step-item active">
                {SVG_ICONS['compass']} 01 SPATIAL BOUNDS
            </div>
            <div class="step-divider"></div>
            <div class="step-item">
                {SVG_ICONS['layers']} 02 DRAW INTERVENTION
            </div>
            <div class="step-divider"></div>
            <div class="step-item">
                {SVG_ICONS['radar']} 03 COMMAND CENTER
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    current_city = st.session_state.get("current_city_query", "Saket, New Delhi")
    radius_km = st.session_state.get("radius_km", 1.2)

    l_left, l_right = st.columns([1.2, 1.2], gap="large")

    with l_left:
        st.markdown(
            """
            <div style="margin-bottom:1rem;">
                <h2 style="font-family:'Space Grotesk',sans-serif;font-size:1.8rem;font-weight:800;color:#FFFFFF;margin-bottom:0.35rem;">
                    Select Study Area Bounds
                </h2>
                <div style="font-size:0.88rem;color:#E5E7EB;line-height:1.5;">
                    Specify target urban node. ShadowCost will fetch vector street networks, OSM building geometries, and canopy layers.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        city_input = st.text_input(
            "Search location",
            value=current_city,
            placeholder="Search city, neighborhood, or spatial coordinates...",
            label_visibility="collapsed"
        )

        if city_input != current_city:
            st.session_state["current_city_query"] = city_input
            st.session_state.pop("intervention_map", None)
            st.rerun()

        st.markdown(
            """
            <div style="display:flex;justify-content:space-between;align-items:center;margin-top:1.1rem;margin-bottom:0.6rem;">
                <div style="font-family:'Space Grotesk',sans-serif;font-size:0.82rem;font-weight:700;color:#FFFFFF;">Preset Urban Nodes</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#9CA3AF;">GeoPandas Ready</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        preset_items = [
            ("Saket, New Delhi", "Dense metro corridor"),
            ("Koramangala, Bengaluru", "High mobility hub"),
            ("Bandra West, Mumbai", "Coastal commercial node"),
            ("Salt Lake, Kolkata", "Planned sector canopy")
        ]

        p_row1_c1, p_row1_c2 = st.columns(2)
        p_row2_c1, p_row2_c2 = st.columns(2)
        grid_cols = [p_row1_c1, p_row1_c2, p_row2_c1, p_row2_c2]

        for idx, (preset_name, preset_desc) in enumerate(preset_items):
            with grid_cols[idx]:
                is_selected = (preset_name.lower() in current_city.lower())
                btn_type = "primary" if is_selected else "secondary"
                if st.button(f"{preset_name}\n({preset_desc})", key=f"loc_preset_btn_{idx}", type=btn_type, use_container_width=True):
                    st.session_state["current_city_query"] = preset_name
                    st.session_state.pop("intervention_map", None)
                    st.rerun()

    # Geocode Location Result
    location_result = geocode_city_with_buffer(current_city, buffer_meters=radius_km * 1000.0)
    if location_result is None:
        st.error("Location could not be resolved. Please enter a valid city or node.")
        return

    center_lat, center_lon, buffer_geom, bbox, display_name = location_result

    with l_right:
        st.markdown(
            f"""
            <div class="glass-panel" style="padding:1.1rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.65rem;">
                    <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:0.88rem;color:#FFFFFF;">Spatial Vector Canvas</div>
                    <div class="badge badge-emerald">{radius_km:.1f} km catchment</div>
                </div>
            """,
            unsafe_allow_html=True
        )

        # Standard Keyless OSM Map Layer
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=14,
            tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            zoom_control=False
        )

        # Inject animated vector style directly into map header
        m.get_root().header.add_child(
            folium.Element("""
            <style>
                @keyframes dash {
                    to { stroke-dashoffset: -30; }
                }
                .animated-vector-path {
                    animation: dash 1.5s linear infinite !important;
                }
            </style>
            """)
        )

        # Apply CSS Filter & Animated Vector Corridor Laser Strokes directly to map tiles
        folium.Element(DARK_TILE_CSS).add_to(m.get_root().header)

        # Sample animated catchment corridor polyline
        corridor_coords = [
            [center_lat - 0.005, center_lon - 0.005],
            [center_lat, center_lon],
            [center_lat + 0.005, center_lon + 0.005]
        ]
        folium.PolyLine(
            locations=corridor_coords,
            color="#10B981",
            weight=5,
            opacity=0.9,
            dash_array="10, 20",
            className="animated-vector-path",
            tooltip="Live Animated Vector Alignment"
        ).add_to(m)

        folium.Circle(
            location=[center_lat, center_lon],
            radius=radius_km * 1000,
            color="#10B981",
            weight=2.5,
            dash_array="10, 20",
            className="animated-vector-path",
            fill=True,
            fill_color="#10B981",
            fill_opacity=0.12
        ).add_to(m)

        folium.Marker(
            [center_lat, center_lon],
            tooltip=display_name,
            icon=folium.Icon(color="green", icon="info-sign")
        ).add_to(m)

        # Explicit height=550 to fix map canvas container
        st_folium(m, key="loc_preview_map", width=None, height=550, returned_objects=[])

        # Bottom HUD Bar with real-time cursor coordinates and projection
        st.markdown(
            f"""
            <div class="map-hud-bar">
                <span>CURSOR: {center_lat:.4f}° N, {center_lon:.4f}° E</span>
                <span>PROJECTION: EPSG:4326 | ZOOM: z=14</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        new_radius = st.slider("Catchment radius (km)", 0.5, 3.0, float(radius_km), 0.1)
        if new_radius != radius_km:
            st.session_state["radius_km"] = new_radius
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

        if st.button("Continue to Draw Intervention →", key="loc_next_btn", type="primary", use_container_width=True):
            if on_next_callback:
                on_next_callback(1)
            st.rerun()
