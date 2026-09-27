"""
components/location_selector.py - Location Selection Screen Component
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
from config import KNOWN_CITIES
from core.geocoding import geocode_city_with_buffer


def render_location_stage(on_next_callback=None):
    """Renders Location Selection Screen with Search, Presets, and Map Preview."""

    st.markdown(
        '<div style="margin-bottom:1.15rem;">'
        '<div style="font-family:\'Space Mono\',monospace;font-size:0.72rem;color:#64748b;font-weight:700;letter-spacing:0.06em;">STEP 1 — LOCATION</div>'
        '<h1 style="font-size:2rem;font-weight:800;color:#0f172a;letter-spacing:-0.03em;margin-top:0.15rem;margin-bottom:0.35rem;">'
        'Where are you planning?'
        '</h1>'
        '<div style="font-size:0.9rem;color:#64748b;max-width:800px;line-height:1.5;">'
        'Choose the area you want to study. ShadowCost pulls the surrounding street network and urban features for spatial analysis.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    current_city = st.session_state.get("current_city_query", "Saket, New Delhi")
    radius_km = st.session_state.get("radius_km", 1.2)

    l_left, l_right = st.columns([1.3, 1], gap="large")

    with l_left:
        city_input = st.text_input(
            "Search location",
            value=current_city,
            placeholder="Search a city, neighborhood, or location...",
            label_visibility="collapsed"
        )

        if city_input != current_city:
            st.session_state["current_city_query"] = city_input
            st.session_state.pop("intervention_map", None)
            st.rerun()

        st.markdown(
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-top:1.1rem;margin-bottom:0.6rem;">'
            '<div style="font-size:0.82rem;font-weight:700;color:#0f172a;">Example locations</div>'
            '<div style="font-size:0.75rem;color:#94a3b8;">Tap to select</div>'
            '</div>',
            unsafe_allow_html=True
        )

        preset_items = [
            ("Saket, New Delhi", "Dense residential · metro corridor"),
            ("Koramangala, Bengaluru", "Mixed-use · high mobility"),
            ("Bandra West, Mumbai", "Coastal · commercial"),
            ("Salt Lake, Kolkata", "Planned sectors · green cover")
        ]

        p_row1_c1, p_row1_c2 = st.columns(2)
        p_row2_c1, p_row2_c2 = st.columns(2)
        grid_cols = [p_row1_c1, p_row1_c2, p_row2_c1, p_row2_c2]

        for idx, (preset_name, preset_desc) in enumerate(preset_items):
            with grid_cols[idx]:
                is_selected = (preset_name.lower() in current_city.lower())
                btn_type = "primary" if is_selected else "secondary"
                if st.button(f"📍 {preset_name}\n({preset_desc})", key=f"preset_btn_{idx}", type=btn_type, use_container_width=True):
                    st.session_state["current_city_query"] = preset_name
                    st.session_state.pop("intervention_map", None)
                    st.rerun()

    # Geocode Location Result
    location_result = geocode_city_with_buffer(current_city, buffer_meters=radius_km * 1000.0)
    if location_result is None:
        st.error("❌ Location could not be resolved. Please try another city or neighborhood.")
        return

    center_lat, center_lon, buffer_geom, bbox, display_name = location_result

    with l_right:
        st.markdown(
            '<div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:14px;padding:1.1rem;">'
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.65rem;">'
            '<div style="font-weight:700;font-size:0.9rem;color:#0f172a;">Selected area</div>'
            f'<div style="font-family:\'Space Mono\',monospace;font-size:0.72rem;background:#eff6ff;color:#2563eb;padding:0.2rem 0.5rem;border-radius:4px;font-weight:700;">{radius_km:.1f} km radius</div>'
            '</div>',
            unsafe_allow_html=True
        )

        m = folium.Map(location=[center_lat, center_lon], zoom_start=14, tiles="OpenStreetMap", zoom_control=False)
        folium.Circle(
            location=[center_lat, center_lon], radius=radius_km * 1000,
            color="#2563eb", weight=2, dash_array="5,5", fill=True, fill_color="#2563eb", fill_opacity=0.1
        ).add_to(m)
        folium.Marker([center_lat, center_lon], tooltip=display_name).add_to(m)

        st_folium(m, key="loc_preview_map", width=None, height=210, returned_objects=[])

        new_radius = st.slider("Analysis radius (km)", 0.5, 3.0, float(radius_km), 0.1)
        if new_radius != radius_km:
            st.session_state["radius_km"] = new_radius
            st.rerun()

        st.markdown(
            f'<div style="font-size:0.78rem;color:#475569;margin-top:0.5rem;border-top:1px solid #f1f5f9;padding-top:0.5rem;">'
            f'📍 <b>Location:</b> {display_name[:50]}<br>'
            f'🎯 <b>Catchment:</b> {radius_km:.1f} km radius around study area'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

        if st.button("Continue to Intervention →", type="primary", use_container_width=True):
            if on_next_callback:
                on_next_callback(2)
            st.rerun()
