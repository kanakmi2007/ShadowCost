"""
components/dashboard.py - Spatial Impact Command Center Workspace (Developer Theme)
Flagship Impact Dashboard Core for ShadowCost
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
from config import CATEGORY_COLORS, SVG_ICONS, OSM_TILES, OSM_ATTR, DARK_TILE_CSS
from core.geocoding import geocode_city_with_buffer
from core.demographics import generate_demographic_features
from core.impact_engine import parse_drawing_geometry, calculate_impacts
from core.ai_synthesizer import call_ai_synthesis, generate_mitigation_badges
from core.scenario_manager import save_scenario, get_scenarios


def draw_radial_arc_gauge(score: int, risk_level: str) -> str:
    """Generates clean SVG radial arc meter card HTML. Stripped raw string with zero trailing tags."""
    color = "#10B981" if score < 30 else ("#FFA500" if score < 60 else "#FF4757")
    stroke_dashoffset = 157.08 * (1.0 - (min(100, max(0, score)) / 100.0))
    gauge_html = (
        f'<div class="glass-panel" style="height:210px;padding:12px;text-align:center;display:flex;flex-direction:column;justify-content:center;align-items:center;">'
        f'<div style="font-family:\'Space Grotesk\',sans-serif;font-size:0.68rem;font-weight:700;color:#9CA3AF;letter-spacing:0.05em;margin-bottom:4px;">EXECUTIVE IMPACT GAUGE</div>'
        f'<div style="position:relative;width:170px;height:95px;margin:0 auto;">'
        f'<svg width="170" height="95" viewBox="0 0 120 70">'
        f'<path d="M 10 60 A 50 50 0 0 1 110 60" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="12" stroke-linecap="round"/>'
        f'<path d="M 10 60 A 50 50 0 0 1 110 60" fill="none" stroke="{color}" stroke-width="12" stroke-linecap="round" stroke-dasharray="157.08" stroke-dashoffset="{stroke_dashoffset}"/>'
        f'</svg>'
        f'<div style="position:absolute;bottom:4px;left:0;right:0;text-align:center;">'
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:1.6rem;font-weight:800;color:#FFFFFF;line-height:1;">{score}<span style="font-size:0.85rem;color:#9CA3AF;">/100</span></div>'
        f'<div style="font-family:\'Space Grotesk\',sans-serif;font-size:0.68rem;font-weight:700;color:{color};margin-top:2px;">{risk_level.upper()} RISK INDEX</div>'
        f'</div>'
        f'</div>'
        f'</div>'
    )
    return gauge_html.strip()





def render_dashboard_stage(on_compare_callback=None, on_export_callback=None):
    """Renders Spatial Impact Command Center Workspace."""

    current_city = st.session_state.get("current_city_query", "Saket, New Delhi")
    radius_km = st.session_state.get("radius_km", 1.2)
    road_width = st.session_state.get("road_width", 25)
    detour_factor = st.session_state.get("detour_factor", 1.35)
    demo_seed = st.session_state.get("demo_seed", 42)
    api_key = st.session_state.get("openai_api_key", "")

    location_result = geocode_city_with_buffer(current_city, buffer_meters=radius_km * 1000.0)
    if location_result is None:
        st.error("Please select a valid location in Step 1 first.")
        return

    center_lat, center_lon, buffer_geom, bbox, display_name = location_result
    demographic_gdf = generate_demographic_features(center_lat, center_lon, int(demo_seed))

    # Add calculated area & exposure attributes for tooltips
    if not demographic_gdf.empty:
        demographic_gdf["area_m2"] = demographic_gdf.geometry.area * 111320.0 * 111320.0 / 10.0
        demographic_gdf["area_m2_str"] = demographic_gdf["area_m2"].apply(lambda x: f"{max(120, int(x)):,} m²")
        demographic_gdf["exposure_idx"] = demographic_gdf["category"].apply(
            lambda c: "HIGH (85/100)" if c == "residential" else ("MODERATE (55/100)" if c == "commercial" else "LOW (20/100)")
        )

    # Parse Drawing & Run Calculations
    map_state = st.session_state.get("intervention_map", {})
    drawn_geom, gem_type = parse_drawing_geometry(map_state)

    impacts = calculate_impacts(
        drawn_geom, gem_type, demographic_gdf,
        road_width=road_width, detour_factor=detour_factor
    )

    idx_score = impacts["shadow_cost_index"]
    risk_lbl = impacts["risk_level"]

    # COMMAND CENTER HEADER
    h_left, h_right = st.columns([2.2, 1])

    with h_left:
        st.markdown(
            f"""
            <div style="margin-bottom:0.85rem;">
                <div style="font-family:'Space Grotesk',sans-serif;font-size:0.75rem;color:#10B981;font-weight:700;letter-spacing:0.08em;display:flex;align-items:center;gap:0.4rem;">
                    {SVG_ICONS['radar']} SPATIAL IMPACT COMMAND CENTER
                </div>
                <h1 style="font-family:'Space Grotesk',sans-serif;font-size:2.1rem;font-weight:800;color:#FFFFFF;letter-spacing:-0.03em;margin-top:0.1rem;margin-bottom:0.25rem;">
                    Command Center Intelligence
                </h1>
                <div style="font-size:0.85rem;color:#E5E7EB;display:flex;align-items:center;gap:0.75rem;">
                    <span>LOCATION: <b>{display_name[:45]}</b></span>
                    <span>•</span>
                    <span style="color:#00D2FF;">{impacts["intervention_name"]} ({impacts["dimension_val"]})</span>
                    <span>•</span>
                    <span class="badge badge-emerald">LIVE MODEL ACTIVE</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with h_right:
        b_c1, b_c2 = st.columns(2)
        with b_c1:
            if st.button("Compare Scenarios", key="dash_compare_btn", use_container_width=True):
                if on_compare_callback:
                    on_compare_callback(3)
                st.rerun()
        with b_c2:
            if st.button("Export Brief", key="dash_export_btn", type="primary", use_container_width=True):
                if on_export_callback:
                    on_export_callback(5)
                st.rerun()

    # TOP ANALYTICS ROW: Executive Impact Gauge (LEFT) + 4 Primary Metric HUD Cards (RIGHT)
    col_gauge, col_metrics = st.columns([1.2, 3.6], gap="medium")

    with col_gauge:
        st.markdown(draw_radial_arc_gauge(idx_score, risk_lbl), unsafe_allow_html=True)

    with col_metrics:
        m1, m2 = st.columns(2)
        m3, m4 = st.columns(2)

        with m1:
            st.metric(
                label="PEOPLE AFFECTED",
                value=impacts["people_affected_str"],
                delta=impacts["people_margin"],
                delta_color="off"
            )
        with m2:
            st.metric(
                label="ADDITIONAL TRAVEL",
                value=impacts["additional_travel_str"],
                delta=impacts["travel_subtext"],
                delta_color="off"
            )
        with m3:
            st.metric(
                label="GREEN CANOPY AFFECTED",
                value=impacts["green_area_str"],
                delta=impacts["green_cover_change_str"],
                delta_color="off"
            )
        with m4:
            st.metric(
                label="AFFECTED ASSETS",
                value=impacts["affected_assets_str"],
                delta=impacts["affected_assets_subtext"],
                delta_color="off"
            )

    st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)

    # WHAT CHANGED HUD STRIP
    scenarios = get_scenarios()
    scen_a = scenarios.get("A")
    scen_b = scenarios.get("B")

    if scen_a and scen_b:
        pop_d = scen_b.get("people_affected", 0) - scen_a.get("people_affected", 0)
        pop_d_str = f"+{pop_d:,}" if pop_d > 0 else f"{pop_d:,}"
        travel_d = scen_b.get("additional_travel_pct", 0) - scen_a.get("additional_travel_pct", 0)
        travel_d_str = f"+{travel_d:.0f}%" if travel_d > 0 else f"{travel_d:.0f}%"
        green_d = scen_b.get("green_area_ha", 0) - scen_a.get("green_area_ha", 0)
        green_d_str = f"+{green_d:.1f} ha" if green_d > 0 else f"{green_d:.1f} ha"

        st.markdown(
            f"""
            <div class="glass-panel" style="padding:0.75rem 1rem;display:flex;align-items:center;gap:1.5rem;margin-bottom:0.75rem;">
                <span style="font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:0.78rem;color:#10B981;">WHAT CHANGED (Slot B vs Slot A):</span>
                <span class="mono" style="font-size:0.82rem;color:#FFFFFF;">Resident Delta: {pop_d_str}</span>
                <span class="mono" style="font-size:0.82rem;color:#00D2FF;">Travel Delta: {travel_d_str}</span>
                <span class="mono" style="font-size:0.82rem;color:#10B981;">Canopy Delta: {green_d_str}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#9CA3AF;margin-bottom:0.6rem;padding:0.4rem 0.75rem;background:rgba(255,255,255,0.02);border:1px solid #1E293B;border-radius:6px;">
                SCENARIO DELTA TRACKING: Save intervention into Slot A & Slot B to render live baseline comparison matrix.
            </div>
            """,
            unsafe_allow_html=True
        )

    # TWO COLUMN MAIN HERO WORKSPACE: OpenStreetMap Dark Vector Map (~60%) + AI Synthesis & Evidence Explorer (~40%)
    r_map, r_info = st.columns([1.4, 1], gap="medium")

    with r_map:
        st.markdown(
            """
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem;">
                <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:0.9rem;color:#FFFFFF;">OpenStreetMap Dark Vector Workspace</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#9CA3AF;">
                    <span style="color:#10B981;">● Vector Corridor</span> &nbsp;<span style="color:#00D2FF;">● Residential</span> &nbsp;<span style="color:#FFA500;">● Commercial</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Standard Keyless OSM Map Layer
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=15,
            tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            control_scale=True
        )

        # Apply CSS Filter directly to map tiles to convert standard OSM to dark mode cleanly
        folium.Element("""
        <style>
            .leaflet-tile-pane {
                filter: brightness(0.6) invert(1) contrast(3) hue-rotate(200deg) saturate(0.3);
            }
        </style>
        """).add_to(m.get_root().header)

        folium.Circle(
            location=[center_lat, center_lon], radius=radius_km * 1000,
            color="#10B981", weight=1.5, dash_array="6,6", fill=False
        ).add_to(m)

        def style_feature(feature):
            cat = feature["properties"].get("category")
            edge, fill = CATEGORY_COLORS.get(cat, CATEGORY_COLORS["other"])
            return {"fillColor": edge, "color": edge, "weight": 1.0, "fillOpacity": 0.35}

        folium.GeoJson(
            demographic_gdf[["osmid", "name", "category", "area_m2_str", "exposure_idx", "geometry"]],
            style_function=style_feature,
            tooltip=folium.GeoJsonTooltip(
                fields=["name", "category", "exposure_idx", "area_m2_str"],
                aliases=["Asset:", "Category:", "Exposure Index:", "Footprint Area:"]
            )
        ).add_to(m)

        is_road = impacts["is_road"]
        is_structure = impacts["is_structure"]

        if is_road and drawn_geom is not None:
            coords = [(p[1], p[0]) for p in drawn_geom.coords]
            folium.PolyLine(coords, color="#10B981", weight=7, opacity=0.95, tooltip="Proposed Alignment").add_to(m)
            folium.CircleMarker(coords[0], radius=7, color="#10B981", fill=True, fill_color="#10B981").add_to(m)
            folium.CircleMarker(coords[-1], radius=7, color="#FF4757", fill=True, fill_color="#FF4757").add_to(m)
        elif is_structure and drawn_geom is not None:
            folium.GeoJson(
                drawn_geom.__geo_interface__,
                style_function=lambda x: {"fillColor": "#00D2FF", "color": "#10B981", "weight": 3, "fillOpacity": 0.45},
                tooltip="Proposed Footprint"
            ).add_to(m)

        # Explicit height=550 map canvas container fix
        st_folium(m, key="impact_command_map", width=None, height=550, returned_objects=[])

        # Bottom Map HUD Bar
        st.markdown(
            f"""
            <div class="map-hud-bar">
                <span>CURSOR: {center_lat:.4f}° N, {center_lon:.4f}° E</span>
                <span>PROJECTION: EPSG:4326 / EPSG:3857 | ZOOM: z=15</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with r_info:
        # AI MITIGATION SYNTHESIS CARD WITH 3 DISTINCT COLOR BADGES
        ai_memo = call_ai_synthesis(
            current_city, impacts["intervention_name"], impacts["dimension_val"],
            impacts["demolished_summary_str"], impacts["additional_travel_str"],
            impacts["people_affected_str"], impacts["green_area_str"],
            impacts["land_overwrite_desc"],
            shadow_cost_index=impacts["shadow_cost_index"], api_key=api_key
        )

        badge_data = generate_mitigation_badges(
            impacts["intervention_name"],
            impacts["people_affected_str"],
            impacts["green_area_str"],
            impacts["additional_travel_str"],
            impacts["shadow_cost_index"]
        )

        st.markdown(
            f"""
            <div class="glass-panel" style="padding:1.1rem;margin-bottom:0.75rem;">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.5rem;">
                    <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:0.9rem;color:#10B981;display:flex;align-items:center;gap:0.4rem;">
                        {SVG_ICONS['sparkles']} AI MITIGATION BRIEFING
                    </div>
                    <span class="badge badge-emerald">POLICY SYNTHESIS</span>
                </div>
                <div style="font-size:0.82rem;color:#E5E7EB;line-height:1.55;margin-bottom:0.85rem;">
                    {ai_memo}
                </div>
                <div style="display:flex;flex-direction:column;gap:0.4rem;">
                    <div class="badge badge-rose" style="width:100%;justify-content:flex-start;">
                        PRIMARY RISK: {badge_data['primary_risk']}
                    </div>
                    <div class="badge badge-emerald" style="width:100%;justify-content:flex-start;">
                        CANOPY MITIGATION: {badge_data['canopy_mitigation']}
                    </div>
                    <div class="badge badge-cyan" style="width:100%;justify-content:flex-start;">
                        RECOMMENDED SHIFT: {badge_data['recommended_shift']}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # DENSE EVIDENCE EXPLORER MATRIX WITH EXPLICIT STATUS TAGS
        st.markdown(
            f"""
            <div class="glass-panel" style="padding:1rem;margin-bottom:0.75rem;">
                <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:0.88rem;color:#FFFFFF;margin-bottom:0.5rem;">
                    EVIDENCE EXPLORER TABLE
                </div>
                <table class="dark-table">
                    <thead>
                        <tr>
                            <th>Lens</th>
                            <th>Status Tag</th>
                            <th>Spatial Metric</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="color:#FF4757;font-weight:700;">Social</td>
                            <td><span class="badge badge-rose">[CRITICAL]</span></td>
                            <td class="mono">{impacts['people_affected_str']} residents</td>
                        </tr>
                        <tr>
                            <td style="color:#10B981;font-weight:700;">Environment</td>
                            <td><span class="badge badge-emerald">[NOMINAL]</span></td>
                            <td class="mono">{impacts['green_area_str']} ({impacts['environment']['tree_canopy_removed_text']})</td>
                        </tr>
                        <tr>
                            <td style="color:#00D2FF;font-weight:700;">Mobility</td>
                            <td><span class="badge badge-cyan">[MODERATE]</span></td>
                            <td class="mono">{impacts['additional_travel_str']} delay</td>
                        </tr>
                        <tr>
                            <td style="color:#FFA500;font-weight:700;">Infrastructure</td>
                            <td><span class="badge badge-amber">[MODERATE]</span></td>
                            <td class="mono">{impacts['affected_assets_str']} structures</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            """,
            unsafe_allow_html=True
        )

        # SLOT SAVE & COMPARE CONTROLS
        s_c1, s_c2 = st.columns(2)
        with s_c1:
            if st.button("Save to Slot A", key="dash_save_a", use_container_width=True):
                save_scenario("A", impacts, f"Slot A ({impacts['intervention_name']})")
                st.success("Saved into Slot A")
        with s_c2:
            if st.button("Save to Slot B", key="dash_save_b", use_container_width=True):
                save_scenario("B", impacts, f"Slot B ({impacts['intervention_name']})")
                st.success("Saved into Slot B")
