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
                tickfont=dict(size=10, color="#9AA4B2", family="Space Grotesk, sans-serif")
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
    color = "#14B8A6" if score < 30 else ("#FFA500" if score < 60 else "#FF4757")
    stroke_dashoffset = 157.08 * (1.0 - (min(100, max(0, score)) / 100.0))
    gauge_html = (
        f'<div style="background:#121826;border:1px solid rgba(255,255,255,0.07);border-radius:10px;height:210px;padding:12px;text-align:center;display:flex;flex-direction:column;justify-content:center;align-items:center;">'
        f'<div style="font-family:\'Space Grotesk\',sans-serif;font-size:0.68rem;font-weight:700;color:#9AA4B2;letter-spacing:0.05em;margin-bottom:4px;">EXECUTIVE IMPACT GAUGE</div>'
        f'<div style="position:relative;width:170px;height:95px;margin:0 auto;">'
        f'<svg width="170" height="95" viewBox="0 0 120 70">'
        f'<path d="M 10 60 A 50 50 0 0 1 110 60" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="12" stroke-linecap="round"/>'
        f'<path d="M 10 60 A 50 50 0 0 1 110 60" fill="none" stroke="{color}" stroke-width="12" stroke-linecap="round" stroke-dasharray="157.08" stroke-dashoffset="{stroke_dashoffset}"/>'
        f'</svg>'
        f'<div style="position:absolute;bottom:4px;left:0;right:0;text-align:center;">'
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:1.6rem;font-weight:800;color:#E6EDF3;line-height:1;">{score}<span style="font-size:0.85rem;color:#9AA4B2;">/100</span></div>'
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

    impacts = base_impacts
    timeline_year = whatif_forecast_year

    idx_score = impacts["shadow_cost_index"]
    risk_lbl = impacts["risk_level"]

    # COMMAND CENTER HEADER
    h_left, h_right = st.columns([2.2, 1])

    with h_left:
        st.markdown(
            f"""
            <div style="margin-bottom:0.85rem;">
                <div style="font-family:'Space Grotesk',sans-serif;font-size:12px;color:#14B8A6;font-weight:700;letter-spacing:0.08em;display:flex;align-items:center;gap:0.4rem;">
                    {SVG_ICONS['radar']} SPATIAL IMPACT COMMAND CENTER
                </div>
                <h1 style="font-family:'Space Grotesk',sans-serif;font-size:34px;font-weight:600;color:#E6EDF3;letter-spacing:-0.02em;margin-top:0.1rem;margin-bottom:0.25rem;">
                    Command Center Intelligence
                </h1>
                <div style="font-size:13.5px;color:#9AA4B2;display:flex;align-items:center;gap:0.75rem;">
                    <span>LOCATION: <b style="color:#E6EDF3;">{display_name[:45]}</b></span>
                    <span>•</span>
                    <span style="color:#5EEAD4;">{impacts["intervention_name"]} ({impacts["dimension_val"]})</span>
                    <span>•</span>
                    <span class="badge badge-emerald">FORECAST: {timeline_year}</span>
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

    # TOP ANALYTICS ROW: Executive Impact Gauge (LEFT) + 4 Primary Metrics (RIGHT)
    col_gauge, col_metrics = st.columns([1.1, 3.7], gap="medium")

    with col_gauge:
        st.markdown(draw_radial_arc_gauge(idx_score, risk_lbl), unsafe_allow_html=True)

    with col_metrics:
        m1, m2 = st.columns(2)
        m3, m4 = st.columns(2)

        with m1:
            st.markdown(
                f"""
                <div style="padding:0.2rem 0.4rem;margin-bottom:0.5rem;">
                    <div style="font-family:'Space Grotesk',sans-serif;font-size:12.5px;font-weight:500;color:#9AA4B2;letter-spacing:0.04em;">PEOPLE AFFECTED</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:34px;font-weight:600;color:#E6EDF3;line-height:1.1;margin-top:2px;">{impacts["people_affected_str"]}</div>
                    <div style="font-size:12px;color:#6B7280;margin-top:2px;">↑ {impacts["people_margin"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with m2:
            st.markdown(
                f"""
                <div style="padding:0.2rem 0.4rem;margin-bottom:0.5rem;">
                    <div style="font-family:'Space Grotesk',sans-serif;font-size:12.5px;font-weight:500;color:#9AA4B2;letter-spacing:0.04em;">ADDITIONAL TRAVEL</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:34px;font-weight:600;color:#E6EDF3;line-height:1.1;margin-top:2px;">{impacts["additional_travel_str"]}</div>
                    <div style="font-size:12px;color:#6B7280;margin-top:2px;">↑ {impacts["travel_subtext"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with m3:
            st.markdown(
                f"""
                <div style="padding:0.2rem 0.4rem;">
                    <div style="font-family:'Space Grotesk',sans-serif;font-size:12.5px;font-weight:500;color:#9AA4B2;letter-spacing:0.04em;">GREEN CANOPY AFFECTED</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:34px;font-weight:600;color:#E6EDF3;line-height:1.1;margin-top:2px;">{impacts["green_area_str"]}</div>
                    <div style="font-size:12px;color:#6B7280;margin-top:2px;">↑ {impacts["green_cover_change_str"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with m4:
            st.markdown(
                f"""
                <div style="padding:0.2rem 0.4rem;">
                    <div style="font-family:'Space Grotesk',sans-serif;font-size:12.5px;font-weight:500;color:#9AA4B2;letter-spacing:0.04em;">AFFECTED ASSETS</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:34px;font-weight:600;color:#E6EDF3;line-height:1.1;margin-top:2px;">{impacts["affected_assets_str"]}</div>
                    <div style="font-size:12px;color:#6B7280;margin-top:2px;">↑ {impacts["affected_assets_subtext"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # COMPACT IMPACT SIGNALS SECTION (Replacing radar visualization)
    soc_bar = max(4, min(100, impacts.get("social_score", 10)))
    mob_bar = max(4, min(100, impacts.get("mobility_score", 10)))
    env_bar = max(4, min(100, impacts.get("env_score", 10)))
    inf_bar = max(4, min(100, impacts.get("infra_score", 10)))

    st.markdown(
        f"""
        <div style="margin-top:0.4rem;margin-bottom:0.75rem;padding:0.6rem 0.8rem;background:#121826;border:1px solid rgba(255,255,255,0.06);border-radius:6px;">
            <div style="font-family:'Space Grotesk',sans-serif;font-size:11px;font-weight:600;color:#9AA4B2;letter-spacing:0.06em;margin-bottom:0.4rem;">IMPACT SIGNALS</div>
            <div style="display:flex;flex-direction:column;gap:0.35rem;">
                <div style="display:flex;align-items:center;gap:0.6rem;font-size:11.5px;font-family:'Space Grotesk',sans-serif;">
                    <span style="width:130px;color:#E6EDF3;font-weight:500;">SOCIAL EXPOSURE</span>
                    <div style="flex:1;background:rgba(255,255,255,0.06);height:4px;border-radius:2px;overflow:hidden;">
                        <div style="background:#14B8A6;width:{soc_bar}%;height:100%;"></div>
                    </div>
                    <span style="width:30px;text-align:right;font-family:'JetBrains Mono',monospace;color:#9AA4B2;">{impacts.get("social_score", 10)}</span>
                </div>
                <div style="display:flex;align-items:center;gap:0.6rem;font-size:11.5px;font-family:'Space Grotesk',sans-serif;">
                    <span style="width:130px;color:#E6EDF3;font-weight:500;">MOBILITY SHIFT</span>
                    <div style="flex:1;background:rgba(255,255,255,0.06);height:4px;border-radius:2px;overflow:hidden;">
                        <div style="background:#14B8A6;width:{mob_bar}%;height:100%;"></div>
                    </div>
                    <span style="width:30px;text-align:right;font-family:'JetBrains Mono',monospace;color:#9AA4B2;">{impacts.get("mobility_score", 10)}</span>
                </div>
                <div style="display:flex;align-items:center;gap:0.6rem;font-size:11.5px;font-family:'Space Grotesk',sans-serif;">
                    <span style="width:130px;color:#E6EDF3;font-weight:500;">ENVIRONMENT</span>
                    <div style="flex:1;background:rgba(255,255,255,0.06);height:4px;border-radius:2px;overflow:hidden;">
                        <div style="background:#14B8A6;width:{env_bar}%;height:100%;"></div>
                    </div>
                    <span style="width:30px;text-align:right;font-family:'JetBrains Mono',monospace;color:#9AA4B2;">{impacts.get("env_score", 10)}</span>
                </div>
                <div style="display:flex;align-items:center;gap:0.6rem;font-size:11.5px;font-family:'Space Grotesk',sans-serif;">
                    <span style="width:130px;color:#E6EDF3;font-weight:500;">INFRASTRUCTURE</span>
                    <div style="flex:1;background:rgba(255,255,255,0.06);height:4px;border-radius:2px;overflow:hidden;">
                        <div style="background:#14B8A6;width:{inf_bar}%;height:100%;"></div>
                    </div>
                    <span style="width:30px;text-align:right;font-family:'JetBrains Mono',monospace;color:#9AA4B2;">{impacts.get("infra_score", 10)}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
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
                <span style="font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:0.78rem;color:#14B8A6;">WHAT CHANGED (Slot B vs Slot A):</span>
                <span class="mono" style="font-size:0.82rem;color:#FFFFFF;">Resident Delta: {pop_d_str}</span>
                <span class="mono" style="font-size:0.82rem;color:#00D2FF;">Travel Delta: {travel_d_str}</span>
                <span class="mono" style="font-size:0.82rem;color:#14B8A6;">Canopy Delta: {green_d_str}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#9CA3AF;margin-bottom:0.6rem;padding:0.4rem 0.75rem;background:rgba(255,255,255,0.02);border:1px solid rgba(107,114,128,0.2);border-radius:6px;">
                SCENARIO DELTA TRACKING: Save intervention into Slot A & Slot B to render live baseline comparison matrix.
            </div>
            """,
            unsafe_allow_html=True
        )

    # TWO COLUMN MAIN HERO WORKSPACE: OpenStreetMap Dark Vector Map (~60%) + AI Synthesis & Evidence Explorer (~40%)
    r_map, r_info = st.columns([1.4, 1], gap="medium")

    with r_map:
        # FEATURE 3: DYNAMIC MAP VECTOR LAYER TOGGLES
        st.markdown(
            """
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem;">
                <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:0.88rem;color:#FFFFFF;">OpenStreetMap Dark Vector Workspace</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        l_c1, l_c2, l_c3, l_c4 = st.columns(4)
        with l_c1:
            show_res = st.checkbox("Residential (Cyan)", value=bool(st.session_state.get("map_show_res", True)), key="dash_toggle_res")
            if show_res != st.session_state.get("map_show_res", True):
                st.session_state["map_show_res"] = show_res
                st.rerun()
        with l_c2:
            show_comm = st.checkbox("Commercial (Amber)", value=bool(st.session_state.get("map_show_comm", True)), key="dash_toggle_comm")
            if show_comm != st.session_state.get("map_show_comm", True):
                st.session_state["map_show_comm"] = show_comm
                st.rerun()
        with l_c3:
            show_canopy = st.checkbox("Canopy (Emerald)", value=bool(st.session_state.get("map_show_canopy", True)), key="dash_toggle_canopy")
            if show_canopy != st.session_state.get("map_show_canopy", True):
                st.session_state["map_show_canopy"] = show_canopy
                st.rerun()
        with l_c4:
            show_detour = st.checkbox("Detour Vector", value=bool(st.session_state.get("map_show_detour", True)), key="dash_toggle_detour")
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

        if show_detour:
            folium.Circle(
                location=[center_lat, center_lon], radius=radius_km * 1000,
                color="#10B981", weight=2, dash_array="10, 20", className="animated-vector-path", fill=False
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
            if is_road and drawn_geom is not None:
                coords = [(p[1], p[0]) for p in drawn_geom.coords]
                folium.PolyLine(
                    locations=coords,
                    color="#10B981",
                    weight=6,
                    opacity=0.95,
                    dash_array="10, 20",
                    className="animated-vector-path",
                    tooltip="Proposed Alignment (Live Animated Vector)"
                ).add_to(m)
                folium.CircleMarker(coords[0], radius=7, color="#10B981", fill=True, fill_color="#10B981").add_to(m)
                folium.CircleMarker(coords[-1], radius=7, color="#FF4757", fill=True, fill_color="#FF4757").add_to(m)
            elif is_structure and drawn_geom is not None:
                folium.GeoJson(
                    drawn_geom.__geo_interface__,
                    style_function=lambda x: {"fillColor": "#00D2FF", "color": "#10B981", "weight": 3, "fillOpacity": 0.45},
                    tooltip="Proposed Footprint"
                ).add_to(m)

        # Explicit height=520 map canvas container fix
        st_folium(m, key="impact_command_map", width=None, height=520, returned_objects=[])

        # FEATURE 2: 10-YEAR PREDICTIVE TIMELINE SIMULATOR SLIDER
        st.markdown(
            f"""
            <div style="margin-top:0.6rem;padding:0.6rem 0.9rem;background:#11161D;border:1px solid rgba(107,114,128,0.2);border-radius:8px;">
                <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:0.8rem;color:#F7F7F5;display:flex;justify-content:space-between;align-items:center;">
                    <span>10-YEAR PREDICTIVE TIMELINE SIMULATOR</span>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#14B8A6;background:rgba(15,118,110,0.15);padding:0.15rem 0.5rem;border-radius:3px;">
                        FORECAST: {timeline_year}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        new_year = st.select_slider(
            "Forecast Horizon Year",
            options=[2026, 2028, 2031, 2035],
            value=timeline_year,
            key="dashboard_timeline_year_slider"
        )
        if new_year != timeline_year:
            st.session_state["timeline_year"] = new_year
            st.rerun()

        year_descs = {
            2026: "2026 (Construction): Peak initial delay multiplier (1.4x), temporary social noise disruption.",
            2028: "2028 (Near-Term): Baseline operational state, initial canopy loss peak.",
            2031: "2031 (Mid-Term): 10% canopy regrowth recovery, 5% transit efficiency gain.",
            2035: "2035 (Long-Term): 20% green buffer regrowth recovery, 15% long-term transit gains."
        }
        st.caption(f"Phase Characteristics: {year_descs[timeline_year]}")

    with r_info:
        # WHAT-IF SCENARIO SIMULATOR WORKSPACE PANEL
        with st.expander("WHAT-IF SCENARIO SIMULATOR", expanded=True):
            # 1. HEADER
            st.markdown(
                f"""
                <div style="margin-bottom:0.6rem;">
                    <div style="font-family:'Space Grotesk',sans-serif;font-size:1.05rem;font-weight:600;color:#E6EDF3;">
                        <span style="color:#14B8A6;">WHAT-IF</span> Scenario Simulator
                    </div>
                    <div style="font-size:12.5px;color:#9AA4B2;margin-top:2px;">
                        Test how planning changes affect projected urban impact. Current: <b style="color:#E6EDF3;">{base_impacts['intervention_name']}</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # 2. PLANNING CONTROLS CONSOLE
            st.markdown("<div style='font-family:\"Space Grotesk\",sans-serif;font-size:11px;font-weight:600;color:#6B7280;letter-spacing:0.06em;margin-bottom:0.25rem;'>PLANNING CONTROLS</div>", unsafe_allow_html=True)

            c_col1, c_col2 = st.columns(2)
            with c_col1:
                new_gb = st.slider("Green Buffer (m)", 0, 20, int(whatif_green_buffer), 1, key="whatif_gb_slider")
                if new_gb != whatif_green_buffer:
                    st.session_state["whatif_green_buffer"] = float(new_gb)
                    st.rerun()
            with c_col2:
                new_row = st.slider("Corridor Width Adj (m)", -5, 5, int(whatif_row_adj), 1, key="whatif_row_slider")
                if new_row != whatif_row_adj:
                    st.session_state["whatif_row_adj"] = float(new_row)
                    st.rerun()

            c_col3, c_col4 = st.columns(2)
            with c_col3:
                new_transit = st.toggle("Public Transit Spur (-15% delay)", value=whatif_transit_spur, key="whatif_transit_toggle")
                if new_transit != whatif_transit_spur:
                    st.session_state["whatif_transit_spur"] = new_transit
                    st.rerun()
            with c_col4:
                new_year = st.select_slider(
                    "Forecast Horizon",
                    options=[2026, 2028, 2031, 2035],
                    value=whatif_forecast_year,
                    key="whatif_year_slider"
                )
                if new_year != whatif_forecast_year:
                    st.session_state["whatif_forecast_year"] = new_year
                    st.rerun()

            btn_col1, btn_col2 = st.columns([1.5, 1])
            with btn_col1:
                if st.button("✦ FIND LOWER-IMPACT ALTERNATIVE", key="btn_find_alternatives", type="primary", use_container_width=True):
                    st.session_state["show_alternatives"] = True
                    st.session_state["cached_alternatives"] = evaluate_lower_impact_alternatives(
                        drawn_geom, gem_type, demographic_gdf, road_width, detour_factor, base_impacts
                    )
                    st.rerun()
            with btn_col2:
                if st.button("Reset Scenario", key="whatif_reset_btn", type="secondary", use_container_width=True):
                    st.session_state["whatif_green_buffer"] = 0.0
                    st.session_state["whatif_row_adj"] = 0.0
                    st.session_state["whatif_transit_spur"] = False
                    st.session_state["whatif_forecast_year"] = 2026
                    st.session_state["show_alternatives"] = False
                    st.session_state.pop("cached_alternatives", None)
                    st.rerun()

            # LOWER MODELED IMPACT ALTERNATIVES SECTION
            if st.session_state.get("show_alternatives"):
                alternatives = st.session_state.get("cached_alternatives", [])

                st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
                st.markdown(
                    """
                    <div style="font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:11.5px;color:#14B8A6;letter-spacing:0.04em;margin-bottom:0.4rem;">
                        FIND A LOWER-IMPACT PLAN
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if not alternatives:
                    st.markdown(
                        """
                        <div style="padding:0.6rem 0.8rem;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:6px;margin-bottom:0.6rem;">
                            <div style="font-family:'Space Grotesk',sans-serif;font-size:11px;font-weight:600;color:#9AA4B2;">
                                NO LOWER-MODELED-IMPACT VARIANT FOUND
                            </div>
                            <div style="font-size:11.5px;color:#6B7280;margin-top:2px;">
                                The tested parameter variations did not produce a lower modeled impact than the current scenario.
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    for alt in alternatives:
                        alt_id = alt["id"]
                        alt_label = alt["label"]
                        alt_desc = alt["desc"]
                        alt_score = alt["score"]
                        score_diff = alt["score_diff"]
                        deltas_str = " · ".join(alt["deltas"]) if alt["deltas"] else "Overall lower modeled impact"

                        st.markdown(
                            f"""
                            <div style="padding:0.55rem 0.75rem;background:#151A21;border:1px solid rgba(20, 184, 166, 0.25);border-radius:6px;margin-bottom:0.45rem;">
                                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.25rem;">
                                    <div>
                                        <div style="font-family:'Space Grotesk',sans-serif;font-size:10.5px;font-weight:700;color:#14B8A6;letter-spacing:0.04em;">{alt_label.upper()}</div>
                                        <div style="font-size:12px;font-weight:600;color:#E6EDF3;margin-top:1px;">{alt_desc}</div>
                                    </div>
                                    <div style="text-align:right;">
                                        <div style="font-family:'JetBrains Mono',monospace;font-size:14px;font-weight:700;color:#E6EDF3;">{alt_score} <span style="font-size:10px;color:#9AA4B2;">/ 100</span></div>
                                        <div style="font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;color:#10B981;">↓ {score_diff} pts</div>
                                    </div>
                                </div>
                                <div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#5EEAD4;margin-bottom:0.35rem;">
                                    {deltas_str}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        if st.button(f"APPLY SCENARIO: {alt_desc}", key=f"btn_apply_alt_{alt_id}", type="secondary", use_container_width=True):
                            st.session_state["whatif_green_buffer"] = alt["gb"]
                            st.session_state["whatif_row_adj"] = alt["row"]
                            st.session_state["whatif_transit_spur"] = alt["transit"]
                            st.session_state["whatif_forecast_year"] = alt["year"]
                            st.rerun()

            st.markdown("<div style='height:0.4rem;'></div>", unsafe_allow_html=True)

            # 3. EXECUTIVE IMPACT COMPARISON
            base_idx = base_impacts["shadow_cost_index"]
            whatif_idx = what_if_impacts["shadow_cost_index"]
            idx_diff = whatif_idx - base_idx

            if base_idx > 0:
                idx_pct = ((whatif_idx - base_idx) / float(base_idx)) * 100.0
            else:
                idx_pct = 0.0

            if idx_diff < 0 or idx_pct < 0:
                diff_color = "#10B981"
                diff_text = f"↓ {abs(idx_pct):.1f}%" if idx_pct != 0 else f"↓ {abs(idx_diff)} pts"
            elif idx_diff > 0 or idx_pct > 0:
                diff_color = "#EF4444"
                diff_text = f"↑ {abs(idx_pct):.1f}%" if idx_pct != 0 else f"↑ {abs(idx_diff)} pts"
            else:
                diff_color = "#9AA4B2"
                diff_text = "NO CHANGE"

            st.markdown(
                f"""
                <div style="padding:0.4rem 0;border-top:1px solid rgba(255,255,255,0.06);border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:0.6rem;display:flex;align-items:center;justify-content:space-between;">
                    <div>
                        <div style="font-family:'Space Grotesk',sans-serif;font-size:11px;font-weight:600;color:#9AA4B2;letter-spacing:0.04em;">EXECUTIVE IMPACT INDEX</div>
                        <div style="display:flex;align-items:baseline;gap:0.5rem;margin-top:2px;">
                            <span style="font-family:'JetBrains Mono',monospace;font-size:26px;font-weight:600;color:#9AA4B2;">{base_idx}</span>
                            <span style="font-size:14px;color:#6B7280;">→</span>
                            <span style="font-family:'JetBrains Mono',monospace;font-size:26px;font-weight:600;color:#E6EDF3;">{whatif_idx}</span>
                            <span style="font-family:'Space Grotesk',sans-serif;font-size:10px;font-weight:500;color:#6B7280;margin-left:2px;">WHAT-IF</span>
                        </div>
                    </div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:700;color:{diff_color};background:rgba(255,255,255,0.03);padding:0.2rem 0.55rem;border-radius:4px;border:1px solid {diff_color}30;white-space:nowrap;">
                        {diff_text}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # 4. DIMENSION DELTA VISUALIZATION (Non-wrapping BASE & WHAT-IF labels)
            lenses = [
                ("SOCIAL EXPOSURE", base_impacts["social_score"], what_if_impacts["social_score"], base_impacts["people_affected"], what_if_impacts["people_affected"]),
                ("MOBILITY IMPACT", base_impacts["mobility_score"], what_if_impacts["mobility_score"], base_impacts["additional_travel_pct"], what_if_impacts["additional_travel_pct"]),
                ("ENVIRONMENT", base_impacts["env_score"], what_if_impacts["env_score"], base_impacts["green_area_ha"], what_if_impacts["green_area_ha"]),
                ("INFRASTRUCTURE", base_impacts["infra_score"], what_if_impacts["infra_score"], base_impacts["affected_assets_count"], what_if_impacts["affected_assets_count"]),
            ]

            lens_rows_html = ""
            for name, b_score, w_score, b_raw, w_raw in lenses:
                s_diff = w_score - b_score
                if b_raw > 0:
                    pct_d = ((w_raw - b_raw) / float(b_raw)) * 100.0
                else:
                    pct_d = 0.0

                if s_diff < 0 or pct_d < 0:
                    badge_c = "#10B981"
                    badge_val = f"↓ {abs(pct_d):.1f}%" if pct_d != 0 else f"↓ {abs(s_diff)} pts"
                elif s_diff > 0 or pct_d > 0:
                    badge_c = "#EF4444"
                    badge_val = f"↑ {abs(pct_d):.1f}%" if pct_d != 0 else f"↑ {abs(s_diff)} pts"
                else:
                    badge_c = "#9AA4B2"
                    badge_val = "0.0%"

                b_bar_width = max(4, min(100, b_score))
                w_bar_width = max(4, min(100, w_score))

                lens_rows_html += f"""
                <div style="margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;font-size:11.5px;font-family:'Space Grotesk',sans-serif;margin-bottom:0.2rem;">
                        <span style="color:#E6EDF3;font-weight:600;letter-spacing:0.02em;">{name}</span>
                        <span style="font-family:'JetBrains Mono',monospace;font-size:11px;color:{badge_c};font-weight:700;">{badge_val}</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:0.4rem;font-family:'JetBrains Mono',monospace;font-size:11px;color:#9AA4B2;margin-bottom:0.15rem;">
                        <span style="white-space:nowrap;width:55px;font-size:10px;font-weight:600;color:#9AA4B2;">BASE</span>
                        <div style="flex:1;background:rgba(255,255,255,0.06);height:4px;border-radius:2px;overflow:hidden;">
                            <div style="background:#6B7280;width:{b_bar_width}%;height:100%;"></div>
                        </div>
                        <span style="width:32px;text-align:right;color:#9AA4B2;">{b_score}</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:0.4rem;font-family:'JetBrains Mono',monospace;font-size:11px;color:#E6EDF3;">
                        <span style="white-space:nowrap;width:55px;font-size:10px;font-weight:600;color:#14B8A6;">WHAT-IF</span>
                        <div style="flex:1;background:rgba(255,255,255,0.06);height:4px;border-radius:2px;overflow:hidden;">
                            <div style="background:#14B8A6;width:{w_bar_width}%;height:100%;"></div>
                        </div>
                        <span style="width:32px;text-align:right;color:#14B8A6;font-weight:700;">{w_score}</span>
                    </div>
                </div>
                """

            st.markdown(lens_rows_html, unsafe_allow_html=True)

            # 5. PRIMARY IMPACT EXPLANATION
            explanation_text = generate_whatif_explanation(base_impacts, what_if_impacts, whatif_green_buffer, whatif_row_adj, whatif_transit_spur, whatif_forecast_year)

            st.markdown(
                f"""
                <div style="margin-top:0.4rem;padding:0.4rem 0.65rem;background:rgba(20, 184, 166, 0.06);border-left:2.5px solid #14B8A6;border-radius:0 4px 4px 0;">
                    <div style="font-family:'Space Grotesk',sans-serif;font-size:10.5px;font-weight:700;color:#14B8A6;letter-spacing:0.04em;">PRIMARY IMPACT DRIVER</div>
                    <div style="font-size:12px;color:#E6EDF3;margin-top:2px;line-height:1.4;">
                        "{explanation_text}"
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

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
            <div style="margin-bottom:0.75rem;padding:0.75rem;background:#121826;border:1px solid rgba(255,255,255,0.06);border-radius:6px;">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.4rem;">
                    <div style="font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:0.85rem;color:#14B8A6;display:flex;align-items:center;gap:0.4rem;">
                        {SVG_ICONS['sparkles']} AI MITIGATION BRIEFING
                    </div>
                    <span class="badge badge-emerald">POLICY SYNTHESIS</span>
                </div>
                <div style="font-size:13px;color:#E6EDF3;line-height:1.5;margin-bottom:0.6rem;">
                    {ai_memo}
                </div>
                <div style="display:flex;flex-direction:column;gap:0.3rem;">
                    <div style="font-size:12px;color:#9AA4B2;padding:0.3rem 0.5rem;background:rgba(255,255,255,0.02);border-left:2px solid #EF4444;border-radius:0 3px 3px 0;">
                        <strong style="color:#E6EDF3;">PRIMARY RISK:</strong> {badge_data['primary_risk']}
                    </div>
                    <div style="font-size:12px;color:#9AA4B2;padding:0.3rem 0.5rem;background:rgba(255,255,255,0.02);border-left:2px solid #10B981;border-radius:0 3px 3px 0;">
                        <strong style="color:#E6EDF3;">CANOPY MITIGATION:</strong> {badge_data['canopy_mitigation']}
                    </div>
                    <div style="font-size:12px;color:#9AA4B2;padding:0.3rem 0.5rem;background:rgba(255,255,255,0.02);border-left:2px solid #00D2FF;border-radius:0 3px 3px 0;">
                        <strong style="color:#E6EDF3;">RECOMMENDED SHIFT:</strong> {badge_data['recommended_shift']}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # COMPACT EVIDENCE EXPLORER ROWS
        st.markdown(
            f"""
            <div style="margin-bottom:0.75rem;padding:0.75rem;background:#121826;border:1px solid rgba(255,255,255,0.06);border-radius:6px;">
                <div style="font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:0.85rem;color:#E6EDF3;margin-bottom:0.4rem;">
                    EVIDENCE EXPLORER
                </div>
                <div style="display:flex;flex-direction:column;gap:0.3rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;padding:0.35rem 0.5rem;background:rgba(255,255,255,0.02);border-radius:4px;font-size:12px;">
                        <span style="color:#E6EDF3;font-weight:600;">Social</span>
                        <span class="badge badge-rose">[CRITICAL]</span>
                        <span style="font-family:'JetBrains Mono',monospace;color:#9AA4B2;">{impacts['people_affected_str']} residents</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;align-items:center;padding:0.35rem 0.5rem;background:rgba(255,255,255,0.02);border-radius:4px;font-size:12px;">
                        <span style="color:#E6EDF3;font-weight:600;">Environment</span>
                        <span class="badge badge-emerald">[NOMINAL]</span>
                        <span style="font-family:'JetBrains Mono',monospace;color:#9AA4B2;">{impacts['green_area_str']} ({impacts['environment']['tree_canopy_removed_text']})</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;align-items:center;padding:0.35rem 0.5rem;background:rgba(255,255,255,0.02);border-radius:4px;font-size:12px;">
                        <span style="color:#E6EDF3;font-weight:600;">Mobility</span>
                        <span class="badge badge-cyan">[MODERATE]</span>
                        <span style="font-family:'JetBrains Mono',monospace;color:#9AA4B2;">{impacts['additional_travel_str']} delay</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;align-items:center;padding:0.35rem 0.5rem;background:rgba(255,255,255,0.02);border-radius:4px;font-size:12px;">
                        <span style="color:#E6EDF3;font-weight:600;">Infrastructure</span>
                        <span class="badge badge-amber">[MODERATE]</span>
                        <span style="font-family:'JetBrains Mono',monospace;color:#9AA4B2;">{impacts['affected_assets_str']} structures</span>
                    </div>
                </div>
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

