"""
components/intervention_setup.py - Intervention Builder Component
"""

import time
import streamlit as st
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
from config import CATEGORY_COLORS
from core.geocoding import geocode_city_with_buffer
from core.demographics import generate_demographic_features
from core.impact_engine import parse_drawing_geometry


def render_setup_stage(on_analyze_callback=None):
    """Renders Scenario Studio workspace with interactive Folium map as the centerpiece."""

    st.markdown(
        '<div style="margin-bottom:1rem;">'
        '<div style="font-family:\'Space Mono\',monospace;font-size:0.72rem;color:#64748b;font-weight:700;letter-spacing:0.06em;">STEP 2 — INTERVENTION</div>'
        '<h1 style="font-size:2rem;font-weight:800;color:#0f172a;letter-spacing:-0.03em;margin-top:0.15rem;margin-bottom:0.35rem;">'
        'Draw your proposed infrastructure'
        '</h1>'
        '<div style="font-size:0.9rem;color:#64748b;">'
        'Use the map toolbar on the top-left to draw a proposed road alignment (Line) or structure footprint (Polygon/Rectangle).'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    current_city = st.session_state.get("current_city_query", "Saket, New Delhi")
    radius_km = st.session_state.get("radius_km", 1.2)
    road_width = st.session_state.get("road_width", 25)
    detour_factor = st.session_state.get("detour_factor", 1.35)
    demo_seed = st.session_state.get("demo_seed", 42)

    location_result = geocode_city_with_buffer(current_city, buffer_meters=radius_km * 1000.0)
    if location_result is None:
        st.error("Please configure a valid location in Step 1 first.")
        return

    center_lat, center_lon, buffer_geom, bbox, display_name = location_result
    demographic_gdf = generate_demographic_features(center_lat, center_lon, int(demo_seed))

    # Parse map state
    map_state = st.session_state.get("intervention_map", {})
    drawn_geom, gem_type = parse_drawing_geometry(map_state)
    is_road = gem_type in ["LineString", "MultiLineString"]
    is_structure = gem_type in ["Polygon", "MultiPolygon"]

    m_left, s_right = st.columns([2.4, 1], gap="medium")

    with m_left:
        # Folium Interactive Map Setup
        m = folium.Map(location=[center_lat, center_lon], zoom_start=15, tiles="OpenStreetMap", control_scale=True)

        folium.Circle(
            location=[center_lat, center_lon], radius=radius_km * 1000,
            color="#2563eb", weight=2, dash_array="5,5", fill=False,
            tooltip=f"{radius_km:.1f} km analysis radius"
        ).add_to(m)

        folium.Marker(
            [center_lat, center_lon], tooltip=display_name,
            icon=folium.Icon(color="blue", icon="crosshairs", prefix="fa")
        ).add_to(m)

        def style_feature(feature):
            cat = feature["properties"].get("category")
            edge, fill = CATEGORY_COLORS.get(cat, CATEGORY_COLORS["other"])
            return {"fillColor": fill, "color": edge, "weight": 1.2, "fillOpacity": 0.55}

        folium.GeoJson(
            demographic_gdf[["osmid", "name", "category", "geometry"]],
            name="Urban Features",
            style_function=style_feature,
            tooltip=folium.GeoJsonTooltip(fields=["name", "category"], aliases=["Asset", "Type"])
        ).add_to(m)

        if is_road and drawn_geom is not None:
            coords = [(p[1], p[0]) for p in drawn_geom.coords]
            folium.PolyLine(coords, color="#2563eb", weight=6, opacity=0.9, tooltip="Proposed Road Corridor").add_to(m)
            folium.CircleMarker(coords[0], radius=6, color="#059669", fill=True, fill_color="#10b981", tooltip="Start").add_to(m)
            folium.CircleMarker(coords[-1], radius=6, color="#e11d48", fill=True, fill_color="#e11d48", tooltip="End").add_to(m)
        elif is_structure and drawn_geom is not None:
            folium.GeoJson(
                drawn_geom.__geo_interface__,
                style_function=lambda x: {"fillColor": "#2563eb", "color": "#1d4ed8", "weight": 3, "fillOpacity": 0.3},
                tooltip="Proposed Footprint"
            ).add_to(m)

        Draw(
            export=False, position="topleft",
            draw_options={"polyline": True, "polygon": True, "rectangle": True, "circle": False, "marker": False, "circlemarker": False},
            edit_options={"edit": True, "remove": True}
        ).add_to(m)

        st_folium(
            m, key="intervention_map", width=None, height=580,
            returned_objects=["all_drawings", "last_active_drawing"]
        )

        st.caption("Legend: 🟩 Green Cover/Park  •  🟦 Commercial Retail  •  🟨 Residential Housing  •  ⬜ Civic Structure  •  🔵 Proposed Alignment")

    with s_right:
        # Scenario Studio Panel
        st.markdown(
            '<div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:14px;padding:1.1rem;margin-bottom:1rem;">'
            '<div style="font-weight:700;font-size:0.92rem;color:#0f172a;margin-bottom:0.25rem;">Define your intervention</div>'
            '<div style="font-size:0.78rem;color:#64748b;margin-bottom:0.85rem;">Spatial corridor assumptions</div>',
            unsafe_allow_html=True
        )

        # Status Badge
        if drawn_geom is None:
            st.markdown(
                '<div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:0.6rem 0.8rem;margin-bottom:0.85rem;">'
                '<div style="font-weight:700;font-size:0.82rem;color:#1e40af;">● Scenario ready</div>'
                '<div style="font-size:0.72rem;color:#3b82f6;margin-top:0.15rem;">Select Polyline (Road) or Polygon (Structure) from map toolbar.</div>'
                '</div>',
                unsafe_allow_html=True
            )
        elif is_road:
            st.markdown(
                f'<div style="background:#ecfdf5;border:1px solid #a7f3d0;border-radius:8px;padding:0.6rem 0.8rem;margin-bottom:0.85rem;">'
                f'<div style="font-weight:700;font-size:0.82rem;color:#047857;">● Road corridor drawn</div>'
                f'<div style="font-size:0.72rem;color:#059669;margin-top:0.15rem;">Line geometry captured • Width: {road_width} m</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div style="background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:0.6rem 0.8rem;margin-bottom:0.85rem;">'
                '<div style="font-weight:700;font-size:0.82rem;color:#b45309;">● Footprint drawn</div>'
                '<div style="font-size:0.72rem;color:#d97706;margin-top:0.15rem;">Polygon geometry captured • Structure scenario</div>'
                '</div>',
                unsafe_allow_html=True
            )

        new_width = st.slider("Corridor width (m)", 10, 50, int(road_width), 1)
        if new_width != road_width:
            st.session_state["road_width"] = new_width
            st.rerun()

        new_detour = st.slider("Baseline detour factor", 1.10, 1.60, float(detour_factor), 0.05)
        if new_detour != detour_factor:
            st.session_state["detour_factor"] = new_detour
            st.rerun()

        if st.button("↺ Reset Drawing", use_container_width=True):
            st.session_state.pop("intervention_map", None)
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Run Impact Analysis →", type="primary", use_container_width=True):
            # Polished Analysis State
            status_placeholder = st.empty()
            steps = [
                "✓ Mapping intervention geometry...",
                "✓ Identifying affected urban assets...",
                "● Calculating spatial impact & detour factors...",
                "○ Preparing impact brief..."
            ]
            for step in steps:
                status_placeholder.info(step)
                time.sleep(0.15)
            status_placeholder.empty()

            if on_analyze_callback:
                on_analyze_callback(3)  # Advance to Impact Report
            st.rerun()
