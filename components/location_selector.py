"""
components/location_selector.py - Location & Spatial Bounds Selection Stage (Developer Theme)
Flagship Location Stage for ShadowCost
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
from config import DARK_TILE_CSS
from core.geocoding import geocode_city_with_buffer


def render_location_stage(on_next_callback=None):
    """Renders Spatial Planning Workspace Location Selection Screen."""

    # 1. COMPACT TECHNICAL PROGRESS INDICATOR
    st.markdown(
        """
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#8B97A6;display:flex;align-items:center;gap:0.75rem;margin-bottom:1.1rem;letter-spacing:0.06em;">
            <span style="color:#14B8A6;font-weight:700;">01  SPATIAL BOUNDS</span>
            <span style="color:#334155;">━━━━━</span>
            <span>02  INTERVENTION</span>
            <span style="color:#334155;">━━━━━</span>
            <span>03  COMMAND CENTER</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    current_city = st.session_state.get("current_city_query", "Saket, New Delhi")
    radius_km = st.session_state.get("radius_km", 1.2)

    # TWO-COLUMN SPATIAL PLANNING WORKSPACE (~40% LEFT, ~60% RIGHT)
    l_left, l_right = st.columns([1, 1.4], gap="large")

    with l_left:
        st.markdown(
            """
            <div style="margin-bottom:0.85rem;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#14B8A6;font-weight:600;letter-spacing:0.08em;margin-bottom:0.25rem;">
                    01 / SPATIAL BOUNDS
                </div>
                <h2 style="font-family:'Inter',sans-serif;font-size:1.35rem;font-weight:600;color:#E8EEF5;margin-bottom:0.3rem;">
                    SELECT STUDY AREA
                </h2>
                <div style="font-family:'Inter',sans-serif;font-size:14px;color:#8B97A6;line-height:1.45;font-weight:400;">
                    Select the urban area you want ShadowCost to analyse.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div style='font-family:\"Inter\",sans-serif;font-size:12px;font-weight:600;color:#E8EEF5;letter-spacing:0.04em;margin-bottom:0.25rem;'>LOCATION</div>", unsafe_allow_html=True)
        city_input = st.text_input(
            "Location",
            value=current_city,
            placeholder="Saket, New Delhi",
            label_visibility="collapsed"
        )

        if city_input != current_city:
            st.session_state["current_city_query"] = city_input
            st.session_state.pop("intervention_map", None)
            st.rerun()

        st.markdown(
            """
            <div style="font-family:'Inter',sans-serif;font-size:13px;font-weight:600;color:#E8EEF5;letter-spacing:0.04em;margin-top:1.1rem;margin-bottom:0.5rem;">
                PRESET URBAN NODES
            </div>
            """,
            unsafe_allow_html=True
        )

        preset_items = [
            ("SAKET", "New Delhi · Dense corridor", "Saket, New Delhi"),
            ("KORAMANGALA", "Bengaluru · Mobility hub", "Koramangala, Bengaluru"),
            ("BANDRA WEST", "Mumbai · Commercial", "Bandra West, Mumbai"),
            ("SALT LAKE", "Kolkata · Planned sector", "Salt Lake, Kolkata")
        ]

        p_row1_c1, p_row1_c2 = st.columns(2)
        p_row2_c1, p_row2_c2 = st.columns(2)
        grid_cols = [p_row1_c1, p_row1_c2, p_row2_c1, p_row2_c2]

        for idx, (title, sub, full_query) in enumerate(preset_items):
            with grid_cols[idx]:
                is_selected = (full_query.lower() in current_city.lower())
                btn_type = "primary" if is_selected else "secondary"
                btn_label = f"{title}\n{sub}"
                if st.button(btn_label, key=f"loc_preset_btn_{idx}", type=btn_type, use_container_width=True):
                    st.session_state["current_city_query"] = full_query
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
            <div style="padding:0.75rem;background:#0D131C;border:1px solid rgba(139,151,166,0.12);border-radius:6px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.55rem;">
                    <div>
                        <div style="font-family:'Inter',sans-serif;font-weight:600;font-size:14px;color:#E8EEF5;">SPATIAL CONTEXT</div>
                        <div style="font-family:'Inter',sans-serif;font-size:13px;color:#14B8A6;margin-top:1px;font-weight:500;">{display_name}</div>
                    </div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:600;letter-spacing:0.08em;color:#14B8A6;background:rgba(20,184,166,0.12);padding:0.2rem 0.55rem;border-radius:4px;display:flex;align-items:center;gap:0.35rem;">
                        <span style="width:6px;height:6px;border-radius:50%;background:#14B8A6;"></span> GEO ENGINE READY
                    </div>
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

        # Catchment corridor polyline
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

        # Render Folium Map Canvas
        st_folium(m, key="loc_preview_map", width=None, height=460, returned_objects=[])

        # Below map technical metadata strip
        st.markdown(
            f"""
            <div style="padding:0.4rem 0.75rem;background:#070A0F;border:1px solid rgba(139,151,166,0.12);border-radius:4px;display:flex;justify-content:space-between;align-items:center;font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#8B97A6;margin-top:0.45rem;margin-bottom:0.55rem;">
                <span>LAT/LON: <strong style="color:#E8EEF5;">{center_lat:.4f}° N, {center_lon:.4f}° E</strong></span>
                <span>PROJECTION: <strong style="color:#E8EEF5;">EPSG:4326</strong></span>
                <span>CATCHMENT: <strong style="color:#14B8A6;">{radius_km:.1f} km</strong></span>
            </div>
            """,
            unsafe_allow_html=True
        )

        new_radius = st.slider("Catchment radius (km)", 0.5, 3.0, float(radius_km), 0.1, key="loc_radius_slider")
        if new_radius != radius_km:
            st.session_state["radius_km"] = new_radius
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)

        if st.button("CONTINUE TO INTERVENTION →", key="loc_next_btn", type="primary", use_container_width=True):
            if on_next_callback:
                on_next_callback(1)
            st.rerun()
