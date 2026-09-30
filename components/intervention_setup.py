"""
components/intervention_setup.py - Intervention Drawing & Scenario Studio Workspace (Developer Theme)
Flagship Intervention Stage for ShadowCost
"""

import time
import streamlit as st
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
from config import CATEGORY_COLORS, SVG_ICONS, OSM_TILES, OSM_ATTR, DARK_TILE_CSS
from core.geocoding import geocode_city_with_buffer
from core.demographics import generate_demographic_features
from core.impact_engine import parse_drawing_geometry


def render_setup_stage(on_analyze_callback=None):
    """Renders Scenario Studio workspace with Keyless OSM Dark interactive Folium map."""

    # STEP PROGRESS DRAWER
    st.markdown(
        f"""
        <div class="step-drawer">
            <div class="step-item">
                {SVG_ICONS['compass']} 01 SPATIAL BOUNDS
            </div>
            <div class="step-divider"></div>
            <div class="step-item active">
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
    road_width = st.session_state.get("road_width", 25)
    detour_factor = st.session_state.get("detour_factor", 1.35)
    demo_seed = st.session_state.get("demo_seed", 42)

    location_result = geocode_city_with_buffer(current_city, buffer_meters=radius_km * 1000.0)
    if location_result is None:
        st.error("Please configure a valid location in Step 1 first.")
        return

    center_lat, center_lon, buffer_geom, bbox, display_name = location_result
    demographic_gdf = generate_demographic_features(center_lat, center_lon, int(demo_seed))

    # Add calculated area & exposure attributes for interactive map tooltips
    if not demographic_gdf.empty:
        demographic_gdf["area_m2"] = demographic_gdf.geometry.area * 111320.0 * 111320.0 / 10.0
        demographic_gdf["area_m2_str"] = demographic_gdf["area_m2"].apply(lambda x: f"{max(120, int(x)):,} m²")
        demographic_gdf["exposure_idx"] = demographic_gdf["category"].apply(
            lambda c: "HIGH (85/100)" if c == "residential" else ("MODERATE (55/100)" if c == "commercial" else "LOW (20/100)")
        )

    # Parse map state
    map_state = st.session_state.get("intervention_map", {})
    drawn_geom, gem_type = parse_drawing_geometry(map_state)
    is_road = gem_type in ["LineString", "MultiLineString"]
    is_structure = gem_type in ["Polygon", "MultiPolygon"]

    m_left, s_right = st.columns([2.4, 1], gap="medium")

    with m_left:
        # FEATURE 3: DYNAMIC MAP VECTOR LAYER TOGGLES
        st.markdown(
            """
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem;">
                <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:0.88rem;color:#FFFFFF;">Scenario Studio Drawing Workspace</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        l_c1, l_c2, l_c3, l_c4 = st.columns(4)
        with l_c1:
            show_res = st.checkbox("Residential (Cyan)", value=bool(st.session_state.get("map_show_res", True)), key="setup_toggle_res")
            if show_res != st.session_state.get("map_show_res", True):
                st.session_state["map_show_res"] = show_res
                st.rerun()
        with l_c2:
            show_comm = st.checkbox("Commercial (Amber)", value=bool(st.session_state.get("map_show_comm", True)), key="setup_toggle_comm")
            if show_comm != st.session_state.get("map_show_comm", True):
                st.session_state["map_show_comm"] = show_comm
                st.rerun()
        with l_c3:
            show_canopy = st.checkbox("Canopy (Emerald)", value=bool(st.session_state.get("map_show_canopy", True)), key="setup_toggle_canopy")
            if show_canopy != st.session_state.get("map_show_canopy", True):
                st.session_state["map_show_canopy"] = show_canopy
                st.rerun()
        with l_c4:
            show_detour = st.checkbox("Detour Vector", value=bool(st.session_state.get("map_show_detour", True)), key="setup_toggle_detour")
            if show_detour != st.session_state.get("map_show_detour", True):
                st.session_state["map_show_detour"] = show_detour
                st.rerun()

        # Standard Keyless OSM Map Layer
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=15,
            tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            control_scale=True
        )

        # Apply CSS Filter & Animated Vector Corridor Laser Strokes directly to map tiles
        folium.Element(DARK_TILE_CSS).add_to(m.get_root().header)

        if show_detour:
            folium.Circle(
                location=[center_lat, center_lon], radius=radius_km * 1000,
                color="#10B981", weight=1.5, dash_array="6,6", fill=False,
                tooltip=f"{radius_km:.1f} km catchment"
            ).add_to(m)

        def style_feature(feature):
            cat = feature["properties"].get("category")
            edge, fill = CATEGORY_COLORS.get(cat, CATEGORY_COLORS["other"])
            return {"fillColor": edge, "color": edge, "weight": 1.0, "fillOpacity": 0.35}

        # Filter demographic features based on active layer toggles
        active_cats = []
        if show_res: active_cats.append("residential")
        if show_comm: active_cats.append("commercial")
        if show_canopy: active_cats.append("park")

        filtered_gdf = demographic_gdf[demographic_gdf.category.isin(active_cats)] if active_cats else demographic_gdf.iloc[0:0]

        if not filtered_gdf.empty:
            folium.GeoJson(
                filtered_gdf[["osmid", "name", "category", "area_m2_str", "exposure_idx", "geometry"]],
                name="Urban Features",
                style_function=style_feature,
                tooltip=folium.GeoJsonTooltip(
                    fields=["name", "category", "exposure_idx", "area_m2_str"],
                    aliases=["Asset:", "Category:", "Exposure Index:", "Footprint Area:"]
                )
            ).add_to(m)

        # High-Contrast Glowing Vector Stroke
        if show_detour:
            if is_road and drawn_geom is not None:
                coords = [(p[1], p[0]) for p in drawn_geom.coords]
                folium.PolyLine(coords, color="#10B981", weight=7, opacity=0.95, tooltip="Proposed Alignment Corridor").add_to(m)
                folium.CircleMarker(coords[0], radius=7, color="#10B981", fill=True, fill_color="#10B981", tooltip="Start Node").add_to(m)
                folium.CircleMarker(coords[-1], radius=7, color="#FF4757", fill=True, fill_color="#FF4757", tooltip="End Node").add_to(m)
            elif is_structure and drawn_geom is not None:
                folium.GeoJson(
                    drawn_geom.__geo_interface__,
                    style_function=lambda x: {"fillColor": "#00D2FF", "color": "#10B981", "weight": 3, "fillOpacity": 0.45},
                    tooltip="Proposed Development Footprint"
                ).add_to(m)

        Draw(
            export=False, position="topleft",
            draw_options={"polyline": True, "polygon": True, "rectangle": True, "circle": False, "marker": False, "circlemarker": False},
            edit_options={"edit": True, "remove": True}
        ).add_to(m)

        # Explicit height=520 map canvas container fix
        st_folium(
            m, key="intervention_map", width=None, height=520,
            returned_objects=["all_drawings", "last_active_drawing"]
        )

        # Map HUD Bar with real-time cursor coordinates and layer status
        st.markdown(
            f"""
            <div class="map-hud-bar">
                <span>CURSOR: {center_lat:.4f}° N, {center_lon:.4f}° E</span>
                <span>LAYERS: [Residential: {'ON' if show_res else 'OFF'} | Commercial: {'ON' if show_comm else 'OFF'} | Canopy: {'ON' if show_canopy else 'OFF'} | Detour: {'ON' if show_detour else 'OFF'}]</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with s_right:
        # Glassmorphic Scenario Control Panel
        st.markdown(
            f"""
            <div class="glass-panel" style="padding:1.1rem;margin-bottom:1rem;">
                <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.4rem;">
                    {SVG_ICONS['layers']}
                    <span style="font-family:'Inter',sans-serif;font-weight:700;font-size:0.95rem;color:#FFFFFF;">Intervention Parameters</span>
                </div>
                <div style="font-size:0.78rem;color:#9CA3AF;margin-bottom:0.85rem;">Corridor & spatial geometry buffer</div>
            """,
            unsafe_allow_html=True
        )

        # Status Badge
        if drawn_geom is None:
            st.markdown(
                """
                <div class="badge badge-cyan" style="width:100%;justify-content:center;padding:0.5rem;margin-bottom:0.85rem;">
                    STATUS: DRAW ALIGNMENT ON MAP
                </div>
                """,
                unsafe_allow_html=True
            )
        elif is_road:
            st.markdown(
                f"""
                <div class="badge badge-emerald" style="width:100%;justify-content:center;padding:0.5rem;margin-bottom:0.85rem;">
                    STATUS: ROAD ALIGNMENT ({road_width}m)
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div class="badge badge-amber" style="width:100%;justify-content:center;padding:0.5rem;margin-bottom:0.85rem;">
                    STATUS: DEVELOPMENT FOOTPRINT
                </div>
                """,
                unsafe_allow_html=True
            )

        new_width = st.slider("Corridor width (m)", 10, 50, int(road_width), 1)
        if new_width != road_width:
            st.session_state["road_width"] = new_width
            st.rerun()

        new_detour = st.slider("Detour multiplier", 1.10, 1.60, float(detour_factor), 0.05)
        if new_detour != detour_factor:
            st.session_state["detour_factor"] = new_detour
            st.rerun()

        if st.button("Reset Geometry", key="setup_reset_btn", use_container_width=True):
            st.session_state.pop("intervention_map", None)
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Run Spatial Analysis [⌘+ENTER] →", key="setup_run_btn", type="primary", use_container_width=True):
            status_placeholder = st.empty()
            steps = [
                "✓ Calculating vector spatial intersection...",
                "✓ Querying GeoPandas demographic buffer...",
                "● Computing 4-lens radar sub-scores...",
                "○ Generating AI Mitigation Briefing..."
            ]
            for step in steps:
                status_placeholder.info(step)
                time.sleep(0.12)
            status_placeholder.empty()

            if on_analyze_callback:
                on_analyze_callback(2)  # Advance to Command Center / Impact Dashboard
            st.rerun()
