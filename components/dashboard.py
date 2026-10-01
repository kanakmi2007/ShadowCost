"""
components/dashboard.py - Spatial Impact Command Center Workspace (Developer Theme)
Flagship Impact Dashboard Core for ShadowCost
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
from config import CATEGORY_COLORS, SVG_ICONS, OSM_TILES, OSM_ATTR, DARK_TILE_CSS
from core.geocoding import geocode_city_with_buffer
from core.demographics import generate_demographic_features
from core.impact_engine import parse_drawing_geometry, calculate_impacts
from core.ai_synthesizer import call_ai_synthesis, generate_mitigation_badges
from core.scenario_manager import get_scenarios, save_scenario
def evaluate_lower_impact_alternatives(
    drawn_geom, gem_type, demographic_gdf, road_width: float, detour_factor: float, base_impacts: dict
) -> list:
    """
    Evaluates a small, deterministic set of candidate parameter variations using the existing impact engine.
    Returns candidate alternatives that produce a lower calculated Shadow Impact Index than base, sorted in ascending order of score.
    """
    base_score = base_impacts["shadow_cost_index"]

    candidates_def = [
        {
            "id": 1,
            "label": "Alternative 01",
            "desc": "Green Buffer +5m",
            "gb": 5.0,
            "row": 0.0,
            "transit": False,
            "year": 2026
        },
        {
            "id": 2,
            "label": "Alternative 02",
            "desc": "Corridor Width -2m",
            "gb": 0.0,
            "row": -2.0,
            "transit": False,
            "year": 2026
        },
        {
            "id": 3,
            "label": "Alternative 03",
            "desc": "Transit Spur ON",
            "gb": 0.0,
            "row": 0.0,
            "transit": True,
            "year": 2026
        }
    ]

    results = []

    for c in candidates_def:
        cand_impacts = calculate_impacts(
            drawn_geom, gem_type, demographic_gdf,
            road_width=road_width, detour_factor=detour_factor,
            green_buffer_offset=c["gb"],
            row_width_adj=c["row"],
            transit_spur=c["transit"],
            forecast_year=c["year"]
        )

        cand_score = cand_impacts["shadow_cost_index"]

        if cand_score < base_score:
            score_diff = base_score - cand_score

            deltas = []
            
            soc_b, soc_c = base_impacts["social_score"], cand_impacts["social_score"]
            if soc_c < soc_b:
                d_pct = int(((soc_b - soc_c) / float(soc_b)) * 100.0) if soc_b > 0 else 0
                deltas.append(f"Social ↓ {d_pct}%")

            mob_b, mob_c = base_impacts["mobility_score"], cand_impacts["mobility_score"]
            if mob_c < mob_b:
                d_pct = int(((mob_b - mob_c) / float(mob_b)) * 100.0) if mob_b > 0 else 0
                deltas.append(f"Mobility ↓ {d_pct}%")

            env_b, env_c = base_impacts["env_score"], cand_impacts["env_score"]
            if env_c < env_b:
                d_pct = int(((env_b - env_c) / float(env_b)) * 100.0) if env_b > 0 else 0
                deltas.append(f"Environment ↓ {d_pct}%")

            inf_b, inf_c = base_impacts["infra_score"], cand_impacts["infra_score"]
            if inf_c < inf_b:
                d_pct = int(((inf_b - inf_c) / float(inf_b)) * 100.0) if inf_b > 0 else 0
                deltas.append(f"Infrastructure ↓ {d_pct}%")

            c["impacts"] = cand_impacts
            c["score"] = cand_score
            c["score_diff"] = score_diff
            c["deltas"] = deltas
            results.append(c)

    results.sort(key=lambda x: x["score"])
    return results


def generate_whatif_explanation(base_impacts: dict, what_if_impacts: dict, gb: float, row: float, transit: bool, year: int) -> str:
    """Generates a deterministic explanation sentence strictly from calculated numerical deltas."""
    reasons = []
    
    if gb > 0:
        env_d = base_impacts["env_score"] - what_if_impacts["env_score"]
        ha_d = base_impacts["green_area_ha"] - what_if_impacts["green_area_ha"]
        if ha_d > 0 or env_d > 0:
            reasons.append(f"Adding a {int(gb)} m green buffer reduces environmental exposure by preserving tree canopy.")
        else:
            reasons.append(f"Adding a {int(gb)} m green buffer creates a spatial buffer offset for the corridor.")
            
    if row != 0:
        if row < 0:
            reasons.append(f"Reducing corridor width by {abs(int(row))} m decreases residential displacement and asset exposure.")
        else:
            reasons.append(f"Increasing corridor width by {int(row)} m expands spatial footprint and infrastructure intersection.")
            
    if transit:
        reasons.append("Activating public transit spur absorbs mobility demand, reducing travel delay by 15%.")
        
    if year > 2026:
        if year == 2028:
            reasons.append("2028 forecast reflects baseline operational state post-construction peak.")
        elif year == 2031:
            reasons.append("2031 forecast incorporates initial 10% canopy regrowth and transit efficiency.")
        elif year == 2035:
            reasons.append("2035 long-term horizon incorporates 20% green canopy regrowth recovery and full transit efficiency.")

    if not reasons:
        return "Baseline intervention parameters active. Adjust parameters above to simulate policy modifications."
        
    return " ".join(reasons)


def draw_plotly_radar_chart(impacts: dict) -> go.Figure:
    """Renders interactive Plotly radar chart with dark transparent background."""
    categories = ['Social', 'Canopy', 'Mobility', 'Infrastructure']
    
    val_social = min(100, max(15, int(impacts.get('people_affected', 0) / 120.0)))
    val_green = min(100, max(15, int(impacts.get('green_area_ha', 0) * 18.0)))
    val_travel = min(100, max(15, int(impacts.get('additional_travel_pct', 0) * 2.2)))
    val_assets = min(100, max(15, int(impacts.get('affected_assets_count', 0) * 12.0)))
    
    values = [val_social, val_green, val_travel, val_assets, val_social]
    cat_closed = categories + [categories[0]]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=cat_closed,
        fill='toself',
        fillcolor='rgba(20, 184, 166, 0.20)',
        line=dict(color='#14B8A6', width=2),
        marker=dict(size=5, color='#5EEAD4'),
        name='Live Spatial Exposure'
    ))
    
    fig.update_layout(
        transition={"duration": 400, "easing": "cubic-in-out"},
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                color="#9AA4B2",
                gridcolor="rgba(154, 164, 178, 0.18)",
                linecolor="rgba(154, 164, 178, 0.25)",
                tickfont=dict(size=8, color="#9AA4B2")
            ),
            angularaxis=dict(
                color="#9AA4B2",
                gridcolor="rgba(154, 164, 178, 0.18)",
                linecolor="rgba(154, 164, 178, 0.25)",
                tickfont=dict(size=10, color="#9AA4B2", family="Inter, sans-serif")
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=30, r=30, t=25, b=25),
        height=210,
        showlegend=False
    )
    return fig


def draw_radial_arc_gauge(score: int, risk_level: str) -> str:
    """Generates clean SVG radial arc meter card HTML. Restrained dark surface."""
    color = "#14B8A6" if score < 30 else ("#5EEAD4" if score < 60 else "#8B97A6")
    stroke_dashoffset = 157.08 * (1.0 - (min(100, max(0, score)) / 100.0))
    gauge_html = (
        f'<div style="background:#0D131C;border:1px solid rgba(139,151,166,0.12);border-radius:6px;height:210px;padding:12px;text-align:center;display:flex;flex-direction:column;justify-content:center;align-items:center;">'
        f'<div style="font-family:\'Inter\',sans-serif;font-size:0.65rem;font-weight:700;color:#8B97A6;letter-spacing:0.06em;margin-bottom:4px;">SHADOW IMPACT INDEX</div>'
        f'<div style="position:relative;width:170px;height:95px;margin:0 auto;">'
        f'<svg width="170" height="95" viewBox="0 0 120 70">'
        f'<path d="M 10 60 A 50 50 0 0 1 110 60" fill="none" stroke="rgba(139,151,166,0.12)" stroke-width="12" stroke-linecap="round"/>'
        f'<path d="M 10 60 A 50 50 0 0 1 110 60" fill="none" stroke="{color}" stroke-width="12" stroke-linecap="round" stroke-dasharray="157.08" stroke-dashoffset="{stroke_dashoffset}"/>'
        f'</svg>'
        f'<div style="position:absolute;bottom:4px;left:0;right:0;text-align:center;">'
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:1.65rem;font-weight:700;color:#E8EEF5;line-height:1;">{score}<span style="font-size:0.85rem;color:#8B97A6;"> / 100</span></div>'
        f'<div style="font-family:\'Inter\',sans-serif;font-size:0.65rem;font-weight:700;color:{color};margin-top:2px;letter-spacing:0.04em;">{risk_level.upper()} RISK INDEX</div>'
        f'</div>'
        f'</div>'
        f'</div>'
    )
    return gauge_html.strip()





def render_dashboard_stage(on_compare_callback=None, on_export_callback=None):
    """Renders Spatial Impact Command Center Workspace (50/50 Side-by-Side Zero-Scroll Layout)."""

    current_city = st.session_state.get("current_city_query", "Saket, New Delhi")
    radius_km = st.session_state.get("radius_km", 1.2)
    road_width = st.session_state.get("road_width", 25)
    detour_factor = st.session_state.get("detour_factor", 1.35)
    demo_seed = st.session_state.get("demo_seed", 42)
    api_key = st.session_state.get("openai_api_key", "")

    # Retrieve What-If Scenario Simulator state variables
    whatif_green_buffer = float(st.session_state.get("whatif_green_buffer", 0.0))
    whatif_row_adj = float(st.session_state.get("whatif_row_adj", 0.0))
    whatif_transit_spur = bool(st.session_state.get("whatif_transit_spur", False))
    whatif_forecast_year = int(st.session_state.get("whatif_forecast_year", 2026))

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

    # Parse Drawing & Run Real-Time Calculations (Base vs What-If)
    map_state = st.session_state.get("intervention_map", {})
    drawn_geom, gem_type = parse_drawing_geometry(map_state)

    base_impacts = calculate_impacts(
        drawn_geom, gem_type, demographic_gdf,
        road_width=road_width, detour_factor=detour_factor,
        green_buffer_offset=0.0,
        row_width_adj=0.0,
        transit_spur=False,
        forecast_year=2026
    )

    what_if_impacts = calculate_impacts(
        drawn_geom, gem_type, demographic_gdf,
        road_width=road_width, detour_factor=detour_factor,
        green_buffer_offset=whatif_green_buffer,
        row_width_adj=whatif_row_adj,
        transit_spur=whatif_transit_spur,
        forecast_year=whatif_forecast_year
    )

    is_what_if_active = (whatif_green_buffer > 0.0 or whatif_row_adj != 0.0 or whatif_transit_spur)
    impacts = what_if_impacts if is_what_if_active else base_impacts
    idx_score = impacts["shadow_cost_index"]
    risk_lbl = impacts["risk_level"]

    # COMPACT COMMAND CENTER TOP BAR
    top_l, top_r = st.columns([3, 1])
    with top_l:
        st.markdown(
            f"""
            <div style="margin-bottom:0.4rem;">
                <div style="font-family:'Inter',sans-serif;font-size:1.2rem;font-weight:600;color:#E8EEF5;display:flex;align-items:center;gap:0.6rem;">
                    Spatial Impact Command Center &bull; <span style="color:#38A169;">{display_name[:40]}</span>
                </div>
                <div style="font-size:12px;color:#8B97A6;margin-top:2px;">
                    Intervention: <b style="color:#E8EEF5;">{impacts["intervention_name"]}</b> ({impacts["dimension_val"]})
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with top_r:
        b1, b2 = st.columns(2)
        with b1:
            if st.button("Compare", key="dash_compare_btn", use_container_width=True):
                if on_compare_callback:
                    on_compare_callback(3)
                st.rerun()
        with b2:
            if st.button("Export Brief", key="dash_export_btn", type="primary", use_container_width=True):
                if on_export_callback:
                    on_export_callback(5)
                st.rerun()

    # 50/50 SIDE-BY-SIDE MAIN WORKSPACE GRID
    col_left, col_right = st.columns([1.05, 0.95], gap="medium")

    # =========================================================
    # LEFT HALF (~50%): MAP CANVAS & LAYER CONTROLS
    # =========================================================
    with col_left:
        # Layer Toggle Checkboxes
        l_c1, l_c2, l_c3, l_c4, l_c5 = st.columns(5)
        with l_c1:
            show_res = st.checkbox("Residential", value=bool(st.session_state.get("map_show_res", True)), key="dash_toggle_res")
        with l_c2:
            show_comm = st.checkbox("Commercial", value=bool(st.session_state.get("map_show_comm", True)), key="dash_toggle_comm")
        with l_c3:
            show_canopy = st.checkbox("Canopy", value=bool(st.session_state.get("map_show_canopy", True)), key="dash_toggle_canopy")
        with l_c4:
            show_ind = st.checkbox("Industrial", value=bool(st.session_state.get("map_show_ind", True)), key="dash_toggle_ind")
        with l_c5:
            show_detour = st.checkbox("Intervention", value=bool(st.session_state.get("map_show_detour", True)), key="dash_toggle_detour")

        st.session_state["map_show_res"] = show_res
        st.session_state["map_show_comm"] = show_comm
        st.session_state["map_show_canopy"] = show_canopy
        st.session_state["map_show_ind"] = show_ind
        st.session_state["map_show_detour"] = show_detour

        # Standard Keyless OSM Map Layer
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=15,
            tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            control_scale=True
        )

        folium.Element(DARK_TILE_CSS).add_to(m.get_root().header)

        if show_detour:
            folium.Circle(
                location=[center_lat, center_lon], radius=radius_km * 1000,
                color="#E53E3E", weight=1.5, dash_array="6, 6", fill=False
            ).add_to(m)

        def style_feature(feature):
            cat = feature["properties"].get("category")
            edge, fill = CATEGORY_COLORS.get(cat, CATEGORY_COLORS["other"])
            return {"fillColor": edge, "color": edge, "weight": 1.0, "fillOpacity": 0.35}

        # Filter demographic features based on dynamic layer toggles
        active_cats = []
        if show_res: active_cats.append("residential")
        if show_comm: active_cats.append("commercial")
        if show_canopy: active_cats.append("park")
        if show_ind: active_cats.append("industrial")

        filtered_gdf = demographic_gdf[demographic_gdf.category.isin(active_cats)] if active_cats else demographic_gdf.iloc[0:0]

        if not filtered_gdf.empty:
            folium.GeoJson(
                filtered_gdf[["osmid", "name", "category", "area_m2_str", "exposure_idx", "geometry"]],
                style_function=style_feature,
                tooltip=folium.GeoJsonTooltip(
                    fields=["name", "category", "exposure_idx", "area_m2_str"],
                    aliases=["Asset:", "Category:", "Exposure Index:", "Footprint Area:"]
                )
            ).add_to(m)

        is_road = impacts["is_road"]
        is_structure = impacts["is_structure"]

        if show_detour:
            # Single Contrasting Color (#E53E3E Coral/Crimson) for App-Made Intervention Alignment
            if is_road and drawn_geom is not None:
                coords = [(p[1], p[0]) for p in drawn_geom.coords]
                folium.PolyLine(
                    locations=coords,
                    color="#E53E3E",
                    weight=6,
                    opacity=0.95,
                    tooltip="Proposed App Intervention Alignment"
                ).add_to(m)
                folium.CircleMarker(coords[0], radius=6, color="#E53E3E", fill=True, fill_color="#E53E3E").add_to(m)
                folium.CircleMarker(coords[-1], radius=6, color="#E53E3E", fill=True, fill_color="#E53E3E").add_to(m)
            elif is_structure and drawn_geom is not None:
                folium.GeoJson(
                    drawn_geom.__geo_interface__,
                    style_function=lambda x: {"fillColor": "#E53E3E", "color": "#E53E3E", "weight": 2.5, "fillOpacity": 0.45},
                    tooltip="Proposed App Intervention Footprint"
                ).add_to(m)

        # Render Map Canvas (640px height to fill left half side-by-side)
        st_folium(m, key="impact_command_map", width=None, height=640, returned_objects=[])

        # Under-map metadata strip
        st.markdown(
            f"""
            <div style="padding:0.35rem 0.65rem;background:#0D131C;border:1px solid rgba(139,151,166,0.12);border-radius:4px;display:flex;justify-content:space-between;align-items:center;font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#8B97A6;margin-top:0.35rem;">
                <span>COORDINATES: <strong style="color:#E8EEF5;">{center_lat:.4f}° N, {center_lon:.4f}° E</strong></span>
                <span>CATCHMENT: <strong style="color:#38A169;">{radius_km:.1f} km</strong></span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =========================================================
    # RIGHT HALF (~50%): DATA, METRICS & WHAT-IF CONTROLS
    # =========================================================
    with col_right:
        # 1. SHADOW IMPACT INDEX & METRICS CARD
        gauge_color = "#38A169" if idx_score < 30 else ("#48BB78" if idx_score < 60 else "#8B97A6")
        st.markdown(
            f"""
            <div style="padding:0.75rem 0.9rem;background:#0D131C;border:1px solid rgba(139,151,166,0.12);border-radius:6px;margin-bottom:0.65rem;">
                <div style="display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(139,151,166,0.12);padding-bottom:0.5rem;margin-bottom:0.55rem;">
                    <div>
                        <div style="font-family:'Inter',sans-serif;font-size:0.65rem;font-weight:700;color:#8B97A6;letter-spacing:0.06em;">SHADOW IMPACT INDEX</div>
                        <div style="font-family:'JetBrains Mono',monospace;font-size:1.6rem;font-weight:700;color:#E8EEF5;line-height:1;margin-top:2px;">
                            {idx_score}<span style="font-size:0.85rem;color:#8B97A6;"> / 100</span>
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <span class="badge badge-emerald" style="font-size:11px;">{risk_lbl.upper()} RISK</span>
                    </div>
                </div>
                <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:0.5rem;text-align:center;">
                    <div style="background:rgba(255,255,255,0.02);padding:0.4rem;border-radius:4px;">
                        <div style="font-size:0.65rem;color:#8B97A6;font-weight:600;">PEOPLE AFFECTED</div>
                        <div style="font-family:'JetBrains Mono',monospace;font-size:1.05rem;font-weight:700;color:#E8EEF5;margin-top:2px;">{impacts["people_affected_str"]}</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.02);padding:0.4rem;border-radius:4px;">
                        <div style="font-size:0.65rem;color:#8B97A6;font-weight:600;">TRAVEL DELAY</div>
                        <div style="font-family:'JetBrains Mono',monospace;font-size:1.05rem;font-weight:700;color:#E8EEF5;margin-top:2px;">{impacts["additional_travel_str"]}</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.02);padding:0.4rem;border-radius:4px;">
                        <div style="font-size:0.65rem;color:#8B97A6;font-weight:600;">GREEN CANOPY</div>
                        <div style="font-family:'JetBrains Mono',monospace;font-size:1.05rem;font-weight:700;color:#E8EEF5;margin-top:2px;">{impacts["green_area_str"]}</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.02);padding:0.4rem;border-radius:4px;">
                        <div style="font-size:0.65rem;color:#8B97A6;font-weight:600;">ASSETS EXPOSED</div>
                        <div style="font-family:'JetBrains Mono',monospace;font-size:1.05rem;font-weight:700;color:#E8EEF5;margin-top:2px;">{impacts["affected_assets_str"]}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # 2. IMPACT SIGNALS (COMPACT 4 BARS)
        soc_bar = max(4, min(100, impacts.get("social_score", 10)))
        mob_bar = max(4, min(100, impacts.get("mobility_score", 10)))
        env_bar = max(4, min(100, impacts.get("env_score", 10)))
        inf_bar = max(4, min(100, impacts.get("infra_score", 10)))

        st.markdown(
            f"""
            <div style="margin-bottom:0.65rem;padding:0.55rem 0.75rem;background:#0D131C;border:1px solid rgba(139,151,166,0.12);border-radius:6px;">
                <div style="font-family:'Inter',sans-serif;font-size:10.5px;font-weight:600;color:#8B97A6;letter-spacing:0.06em;margin-bottom:0.35rem;">SPATIAL IMPACT SIGNALS</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.4rem 0.8rem;">
                    <div style="display:flex;align-items:center;gap:0.4rem;font-size:11px;">
                        <span style="width:75px;color:#E8EEF5;">Social:</span>
                        <div style="flex:1;background:rgba(255,255,255,0.05);height:4px;border-radius:2px;overflow:hidden;">
                            <div style="background:#38A169;width:{soc_bar}%;height:100%;"></div>
                        </div>
                        <span style="font-family:'JetBrains Mono',monospace;color:#8B97A6;width:25px;text-align:right;">{impacts.get("social_score", 10)}</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:0.4rem;font-size:11px;">
                        <span style="width:75px;color:#E8EEF5;">Mobility:</span>
                        <div style="flex:1;background:rgba(255,255,255,0.05);height:4px;border-radius:2px;overflow:hidden;">
                            <div style="background:#319795;width:{mob_bar}%;height:100%;"></div>
                        </div>
                        <span style="font-family:'JetBrains Mono',monospace;color:#8B97A6;width:25px;text-align:right;">{impacts.get("mobility_score", 10)}</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:0.4rem;font-size:11px;">
                        <span style="width:75px;color:#E8EEF5;">Environment:</span>
                        <div style="flex:1;background:rgba(255,255,255,0.05);height:4px;border-radius:2px;overflow:hidden;">
                            <div style="background:#48BB78;width:{env_bar}%;height:100%;"></div>
                        </div>
                        <span style="font-family:'JetBrains Mono',monospace;color:#8B97A6;width:25px;text-align:right;">{impacts.get("env_score", 10)}</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:0.4rem;font-size:11px;">
                        <span style="width:75px;color:#E8EEF5;">Infrastructure:</span>
                        <div style="flex:1;background:rgba(255,255,255,0.05);height:4px;border-radius:2px;overflow:hidden;">
                            <div style="background:#DD6B20;width:{inf_bar}%;height:100%;"></div>
                        </div>
                        <span style="font-family:'JetBrains Mono',monospace;color:#8B97A6;width:25px;text-align:right;">{impacts.get("infra_score", 10)}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # 3. WHAT-IF SCENARIO CONSOLE EXPANDER
        with st.expander("WHAT-IF SCENARIO CONSOLE", expanded=True):
            w_c1, w_c2 = st.columns(2)
            with w_c1:
                new_gb = st.slider("Green Buffer (m)", 0, 20, int(whatif_green_buffer), 1, key="whatif_gb_slider")
                if new_gb != whatif_green_buffer:
                    st.session_state["whatif_green_buffer"] = float(new_gb)
                    st.rerun()
            with w_c2:
                new_row = st.slider("Corridor Width Adj (m)", -5, 5, int(whatif_row_adj), 1, key="whatif_row_slider")
                if new_row != whatif_row_adj:
                    st.session_state["whatif_row_adj"] = float(new_row)
                    st.rerun()

            w_c3, w_c4 = st.columns(2)
            with w_c3:
                new_transit = st.toggle("Public Transit Spur", value=whatif_transit_spur, key="whatif_transit_toggle")
                if new_transit != whatif_transit_spur:
                    st.session_state["whatif_transit_spur"] = new_transit
                    st.rerun()
            with w_c4:
                btn_find, btn_rst = st.columns(2)
                with btn_find:
                    if st.button("Find Alt", key="btn_find_alternatives", type="primary", use_container_width=True):
                        st.session_state["show_alternatives"] = True
                        st.session_state["cached_alternatives"] = evaluate_lower_impact_alternatives(
                            drawn_geom, gem_type, demographic_gdf, road_width, detour_factor, base_impacts
                        )
                        st.rerun()
                with btn_rst:
                    if st.button("Reset", key="whatif_reset_btn", type="secondary", use_container_width=True):
                        st.session_state["whatif_green_buffer"] = 0.0
                        st.session_state["whatif_row_adj"] = 0.0
                        st.session_state["whatif_transit_spur"] = False
                        st.session_state["show_alternatives"] = False
                        st.session_state.pop("cached_alternatives", None)
                        st.rerun()

            # Display alternatives if triggered
            if st.session_state.get("show_alternatives"):
                alternatives = st.session_state.get("cached_alternatives", [])
                if alternatives:
                    for alt in alternatives:
                        st.markdown(
                            f"""
                            <div style="padding:0.45rem 0.65rem;background:#121824;border:1px solid #38A169;border-radius:4px;margin-bottom:0.35rem;display:flex;justify-content:space-between;align-items:center;">
                                <div>
                                    <strong style="color:#38A169;font-size:11px;">{alt['label']}:</strong> <span style="color:#E8EEF5;font-size:11.5px;">{alt['desc']}</span>
                                </div>
                                <div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#48BB78;font-weight:700;">Score: {alt['score']} (↓ {alt['score_diff']} pts)</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        if st.button(f"Apply {alt['desc']}", key=f"btn_apply_alt_{alt['id']}", type="secondary", use_container_width=True):
                            st.session_state["whatif_green_buffer"] = alt["gb"]
                            st.session_state["whatif_row_adj"] = alt["row"]
                            st.session_state["whatif_transit_spur"] = alt["transit"]
                            st.rerun()

        # 4. AI POLICY BRIEFING NOTE
        ai_memo = call_ai_synthesis(
            current_city, impacts["intervention_name"], impacts["dimension_val"],
            impacts["demolished_summary_str"], impacts["additional_travel_str"],
            impacts["people_affected_str"], impacts["green_area_str"],
            impacts["land_overwrite_desc"],
            shadow_cost_index=impacts["shadow_cost_index"], api_key=api_key
        )

        st.markdown(
            f"""
            <div style="padding:0.65rem 0.85rem;background:#0D131C;border:1px solid rgba(139,151,166,0.12);border-radius:6px;margin-bottom:0.65rem;">
                <div style="font-family:'Inter',sans-serif;font-weight:600;font-size:0.8rem;color:#38A169;margin-bottom:0.35rem;display:flex;align-items:center;gap:0.4rem;">
                    {SVG_ICONS['sparkles']} AI MITIGATION BRIEFING
                </div>
                <div style="font-size:11.5px;color:#E8EEF5;line-height:1.45;">
                    {ai_memo}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # 5. SAVE SLOT A / SLOT B CONTROLS
        s_c1, s_c2 = st.columns(2)
        with s_c1:
            if st.button("Save into Slot A", key="dash_save_a", use_container_width=True):
                sav_data = dict(impacts)
                sav_data["drawn_geom"] = drawn_geom
                sav_data["gem_type"] = gem_type
                sav_data["center_lat"] = center_lat
                sav_data["center_lon"] = center_lon
                sav_data["city_name"] = current_city
                save_scenario("A", sav_data, f"Slot A ({impacts['intervention_name']})")
                st.success("Saved to Slot A")
        with s_c2:
            if st.button("Save into Slot B", key="dash_save_b", use_container_width=True):
                sav_data = dict(impacts)
                sav_data["drawn_geom"] = drawn_geom
                sav_data["gem_type"] = gem_type
                sav_data["center_lat"] = center_lat
                sav_data["center_lon"] = center_lon
                sav_data["city_name"] = current_city
                save_scenario("B", sav_data, f"Slot B ({impacts['intervention_name']})")
                st.success("Saved to Slot B")



