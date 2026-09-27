"""
components/dashboard.py - Impact Report Component (Teal + Black Theme)
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
from config import CATEGORY_COLORS
from core.geocoding import geocode_city_with_buffer
from core.demographics import generate_demographic_features
from core.impact_engine import parse_drawing_geometry, calculate_impacts
from core.ai_synthesizer import call_ai_synthesis
from core.scenario_manager import save_scenario, get_scenarios


def render_dashboard_stage(on_compare_callback=None, on_export_callback=None):
    """Renders Impact Report with Impact Index, Insights, Mitigations, and Map."""

    current_city = st.session_state.get("current_city_query", "Saket, New Delhi")
    radius_km = st.session_state.get("radius_km", 1.2)
    road_width = st.session_state.get("road_width", 25)
    detour_factor = st.session_state.get("detour_factor", 1.35)
    demo_seed = st.session_state.get("demo_seed", 42)
    api_key = st.session_state.get("openai_api_key", "")

    location_result = geocode_city_with_buffer(current_city, buffer_meters=radius_km * 1000.0)
    if location_result is None:
        st.error("Please select a location in Step 1 first.")
        return

    center_lat, center_lon, buffer_geom, bbox, display_name = location_result
    demographic_gdf = generate_demographic_features(center_lat, center_lon, int(demo_seed))

    # Parse Drawing & Run Calculations
    map_state = st.session_state.get("intervention_map", {})
    drawn_geom, gem_type = parse_drawing_geometry(map_state)

    impacts = calculate_impacts(
        drawn_geom, gem_type, demographic_gdf,
        road_width=road_width, detour_factor=detour_factor
    )

    idx_score = impacts["cost"]["shadow_cost_index"]
    impact_lbl = impacts["cost"]["impact_level"]

    # FEATURE 7 — SCENARIO SNAPSHOT HEADER
    h_left, h_right = st.columns([2, 1])

    with h_left:
        st.markdown(
            '<div style="margin-bottom:1rem;">'
            '<div style="font-family:\'Space Mono\',monospace;font-size:0.72rem;color:#0F766E;font-weight:700;letter-spacing:0.06em;">IMPACT REPORT</div>'
            '<h1 style="font-size:2.2rem;font-weight:800;color:#111111;letter-spacing:-0.03em;margin-top:0.15rem;margin-bottom:0.25rem;">'
            'Scenario Impact Report'
            '</h1>'
            f'<div style="font-size:0.88rem;color:#4B5563;">📍 <b>{display_name[:45]}</b> &nbsp;·&nbsp; {impacts["intervention_name"]} &nbsp;·&nbsp; <span style="color:#0F766E;font-weight:700;">● Analyzed</span></div>'
            '</div>',
            unsafe_allow_html=True
        )

    with h_right:
        b_c1, b_c2 = st.columns(2)
        with b_c1:
            if st.button("⇄ Compare", use_container_width=True):
                if on_compare_callback:
                    on_compare_callback(4)
                st.rerun()
        with b_c2:
            if st.button("⬇ Export", type="primary", use_container_width=True):
                if on_export_callback:
                    on_export_callback(6)
                st.rerun()

    # Top KPI Row (4 Metric Cards + FEATURE 1: IMPACT INDEX)
    k_col, score_col = st.columns([3, 1], gap="medium")

    with k_col:
        k1, k2, k3, k4 = st.columns(4)

        with k1:
            st.metric(
                label="👥 PEOPLE AFFECTED",
                value=impacts["people_affected_str"],
                delta=impacts["people_margin"],
                delta_color="off"
            )

        with k2:
            st.metric(
                label="🧭 ADDITIONAL TRAVEL",
                value=impacts["additional_travel_str"],
                delta=impacts["travel_subtext"],
                delta_color="off"
            )

        with k3:
            st.metric(
                label="🍃 GREEN AREA AFFECTED",
                value=impacts["green_area_str"],
                delta=impacts["green_cover_change_str"],
                delta_color="off"
            )

        with k4:
            st.metric(
                label="🏢 AFFECTED ASSETS",
                value=impacts["affected_assets_str"],
                delta=impacts["affected_assets_subtext"],
                delta_color="off"
            )

    with score_col:
        # FEATURE 1 — SHADOW IMPACT INDEX RING/BOX
        st.markdown(
            '<div style="background:#FFFFFF;border:2px solid #0F766E;border-radius:14px;padding:1rem;text-align:center;">'
            '<div style="font-family:\'Space Mono\',monospace;font-size:0.68rem;color:#4B5563;font-weight:700;letter-spacing:0.05em;">SHADOW IMPACT INDEX</div>'
            f'<div style="font-size:2.2rem;font-weight:800;color:#0F766E;line-height:1.1;margin-top:0.2rem;">{idx_score}<span style="font-size:1rem;color:#6B7280;">/100</span></div>'
            f'<div style="font-size:0.75rem;font-weight:700;color:#2A2A2A;margin-top:0.25rem;">{impact_lbl} Modeled Impact</div>'
            '</div>',
            unsafe_allow_html=True
        )

        with st.expander("Why this index score?", expanded=False):
            st.caption(f"Index score of {idx_score}/100 is derived from spatial exposure intensity across displaced residents ({impacts['people_affected']}), canopy loss ({impacts['green_area_str']}), and trip rerouting multipliers.")

    st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)

    # FEATURE 5 — KEY INSIGHT CARD
    st.markdown(
        '<div style="background:#CCFBF1;border:1px solid #99F6E4;border-radius:12px;padding:0.85rem 1.1rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.75rem;">'
        '<div style="font-size:0.88rem;color:#0F766E;line-height:1.4;">'
        f'<b>KEY INSIGHT:</b> {impacts["intervention_name"]} primarily impacts <b>{impacts["people_affected_str"]} residents</b> in the exposure corridor with a <b>{impacts["additional_travel_str"]} travel delta</b>.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)

    # FEATURE 4 — "WHAT CHANGED?" DELTA SECTION
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
            '<div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:0.75rem 1rem;font-size:0.82rem;color:#4b5563;margin-bottom:0.75rem;">'
            f'<b>WHAT CHANGED (Scenario B vs A):</b> &nbsp; 👥 {pop_d_str} residents exposed &nbsp;·&nbsp; 🧭 {travel_d_str} travel distance &nbsp;·&nbsp; 🍃 {green_d_str} green cover'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        st.caption("💡 **Baseline delta tracking:** Save an active scenario into Slot A and Slot B to view automatic baseline comparison deltas.")

    # Two Column Layout: Map Left (~60%), Category Breakdown Right (~40%)
    r_map, r_info = st.columns([1.35, 1], gap="medium")

    with r_map:
        st.markdown(
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;">'
            '<div style="font-weight:700;font-size:0.92rem;color:#111111;">Spatial Impact Map</div>'
            '<div style="font-size:0.75rem;color:#4B5563;"><span style="color:#0F766E;">● Proposed</span> &nbsp;<span style="color:#111111;">● Affected</span> &nbsp;<span style="color:#14B8A6;">● Green</span></div>'
            '</div>',
            unsafe_allow_html=True
        )

        m = folium.Map(location=[center_lat, center_lon], zoom_start=15, tiles="OpenStreetMap", control_scale=True)
        folium.Circle(
            location=[center_lat, center_lon], radius=radius_km * 1000,
            color="#0F766E", weight=2, dash_array="5,5", fill=False
        ).add_to(m)

        def style_feature(feature):
            cat = feature["properties"].get("category")
            edge, fill = CATEGORY_COLORS.get(cat, CATEGORY_COLORS["other"])
            return {"fillColor": fill, "color": edge, "weight": 1.2, "fillOpacity": 0.55}

        folium.GeoJson(
            demographic_gdf[["osmid", "name", "category", "geometry"]],
            style_function=style_feature,
            tooltip=folium.GeoJsonTooltip(fields=["name", "category"], aliases=["Asset", "Type"])
        ).add_to(m)

        is_road = impacts["is_road"]
        is_structure = impacts["is_structure"]

        if is_road and drawn_geom is not None:
            coords = [(p[1], p[0]) for p in drawn_geom.coords]
            folium.PolyLine(coords, color="#0F766E", weight=6, opacity=0.9, tooltip="Proposed Alignment").add_to(m)
            folium.CircleMarker(coords[0], radius=6, color="#14B8A6", fill=True, fill_color="#14B8A6").add_to(m)
            folium.CircleMarker(coords[-1], radius=6, color="#111111", fill=True, fill_color="#111111").add_to(m)
        elif is_structure and drawn_geom is not None:
            folium.GeoJson(
                drawn_geom.__geo_interface__,
                style_function=lambda x: {"fillColor": "#0F766E", "color": "#0F766E", "weight": 3, "fillOpacity": 0.3},
                tooltip="Proposed Footprint"
            ).add_to(m)

        st_folium(m, key="impact_results_map", width=None, height=540, returned_objects=[])

    with r_info:
        # Social Category Breakdown
        st.markdown(
            '<div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:1rem;margin-bottom:0.75rem;">'
            '<div style="font-weight:700;font-size:0.88rem;color:#111111;margin-bottom:0.5rem;">👥 Social</div>'
            f'<div style="font-size:0.84rem;color:#4B5563;display:flex;justify-content:space-between;padding:0.25rem 0;border-bottom:1px solid #f1f5f9;"><span>Residents in exposure zone</span><b>{impacts["social"]["exposure_residents"]:,}</b></div>'
            f'<div style="font-size:0.84rem;color:#4B5563;display:flex;justify-content:space-between;padding:0.25rem 0;border-bottom:1px solid #f1f5f9;"><span>Pedestrian routes disrupted</span><b>{impacts["social"]["pedestrian_routes_disrupted"]}</b></div>'
            f'<div style="font-size:0.84rem;color:#4B5563;display:flex;justify-content:space-between;padding:0.25rem 0;"><span>Community assets nearby</span><b>{impacts["social"]["community_assets_text"]}</b></div>'
            '</div>',
            unsafe_allow_html=True
        )

        # Environment Category Breakdown
        st.markdown(
            '<div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:1rem;margin-bottom:0.75rem;">'
            '<div style="font-weight:700;font-size:0.88rem;color:#111111;margin-bottom:0.5rem;">🍃 Environment</div>'
            f'<div style="font-size:0.84rem;color:#4B5563;display:flex;justify-content:space-between;padding:0.25rem 0;border-bottom:1px solid #f1f5f9;"><span>Tree canopy removed</span><b>{impacts["environment"]["tree_canopy_removed_text"]}</b></div>'
            f'<div style="font-size:0.84rem;color:#4B5563;display:flex;justify-content:space-between;padding:0.25rem 0;border-bottom:1px solid #f1f5f9;"><span>Green cover change</span><b>-{impacts["environment"]["green_cover_change_pct"]}%</b></div>'
            f'<div style="font-size:0.84rem;color:#4B5563;display:flex;justify-content:space-between;padding:0.25rem 0;"><span>Heat exposure risk</span><b>{impacts["environment"]["heat_exposure_risk"]}</b></div>'
            '</div>',
            unsafe_allow_html=True
        )

        # Mobility Category Breakdown
        st.markdown(
            '<div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:1rem;margin-bottom:0.75rem;">'
            '<div style="font-weight:700;font-size:0.88rem;color:#111111;margin-bottom:0.5rem;">🧭 Mobility</div>'
            f'<div style="font-size:0.84rem;color:#4B5563;display:flex;justify-content:space-between;padding:0.25rem 0;border-bottom:1px solid #f1f5f9;"><span>Avg. added travel distance</span><b>+{impacts["mobility"]["avg_added_distance_km"]} km</b></div>'
            f'<div style="font-size:0.84rem;color:#4B5563;display:flex;justify-content:space-between;padding:0.25rem 0;border-bottom:1px solid #f1f5f9;"><span>Trips rerouted daily</span><b>~{impacts["mobility"]["trips_rerouted_daily"]:,}</b></div>'
            f'<div style="font-size:0.84rem;color:#4B5563;display:flex;justify-content:space-between;padding:0.25rem 0;"><span>Peak-hour delay</span><b>+{impacts["mobility"]["peak_hour_delay_pct"]:.0f}%</b></div>'
            '</div>',
            unsafe_allow_html=True
        )

        # FEATURE 6 — POTENTIAL MITIGATION CONSIDERATIONS
        with st.expander("🛡️ Potential Mitigation Considerations", expanded=False):
            st.markdown(
                "• **Pedestrian Access:** Maintain continuous footpaths and marked pedestrian crossings along alignment.\n"
                "• **Canopy Protection:** Implement a 5-meter green buffer to protect high-density tree clusters.\n"
                "• **Phased Construction:** Schedule construction off-peak to limit daily trip rerouting delays."
            )

        # AI Impact Brief Box
        ai_memo = call_ai_synthesis(
            current_city, impacts["intervention_name"], impacts["dimension_val"],
            impacts["demolished_summary_str"], impacts["additional_travel_str"],
            impacts["people_affected_str"], impacts["green_area_str"],
            impacts["land_overwrite_desc"],
            shadow_cost_index=impacts["cost"]["shadow_cost_index"], api_key=api_key
        )

        st.markdown(
            '<div style="background:#CCFBF1;border:1px solid #99F6E4;border-radius:12px;padding:1rem;margin-bottom:0.75rem;">'
            '<div style="font-weight:700;font-size:0.88rem;color:#0F766E;margin-bottom:0.4rem;">🤖 AI Impact Brief</div>'
            f'<div style="font-size:0.83rem;color:#115E59;line-height:1.55;">{ai_memo}</div>'
            '</div>',
            unsafe_allow_html=True
        )

        # Slot Save & Compare Action
        s_c1, s_c2 = st.columns(2)
        with s_c1:
            if st.button("💾 Save to Slot A", use_container_width=True):
                save_scenario("A", impacts, f"Scenario A ({impacts['intervention_name']})")
                st.success("Saved to Slot A")
        with s_c2:
            if st.button("💾 Save to Slot B", use_container_width=True):
                save_scenario("B", impacts, f"Scenario B ({impacts['intervention_name']})")
                st.success("Saved to Slot B")

        if st.button("Compare alternative scenarios →", use_container_width=True):
            if on_compare_callback:
                on_compare_callback(4)
            st.rerun()
