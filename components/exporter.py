"""
components/exporter.py - Export Scenario Component (Teal + Black Theme)
"""

import json
from datetime import datetime
import pandas as pd
import streamlit as st
from core.geocoding import geocode_city_with_buffer
from core.demographics import generate_demographic_features
from core.impact_engine import parse_drawing_geometry, calculate_impacts
from core.ai_synthesizer import call_ai_synthesis


def render_exporter_stage():
    """Renders Export Scenario Screen with high-contrast buttons and 3 cards."""

    st.markdown(
        '<div style="margin-bottom:1.25rem;">'
        '<div style="font-family:\'Space Mono\',monospace;font-size:0.72rem;color:#0F766E;font-weight:700;letter-spacing:0.06em;">EXPORT SCENARIO</div>'
        '<h1 style="font-size:2rem;font-weight:800;color:#111111;letter-spacing:-0.03em;margin-top:0.15rem;margin-bottom:0.35rem;">'
        'Download your analysis'
        '</h1>'
        '<div style="font-size:0.9rem;color:#4B5563;">'
        'Export complete scenario spatial metrics, impact indicators, and executive summaries for decision-makers.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

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

    map_state = st.session_state.get("intervention_map", {})
    drawn_geom, gem_type = parse_drawing_geometry(map_state)

    if drawn_geom is None:
        st.info("💡 **Run an impact analysis first to generate exports.** Draw a corridor or footprint on the Scenario page and click Run Impact Analysis.")

    impacts = calculate_impacts(
        drawn_geom, gem_type, demographic_gdf,
        road_width=road_width, detour_factor=detour_factor
    )

    ai_memo = call_ai_synthesis(
        current_city, impacts["intervention_name"], impacts["dimension_val"],
        impacts["demolished_summary_str"], impacts["additional_travel_str"],
        impacts["people_affected_str"], impacts["green_area_str"],
        impacts["land_overwrite_desc"],
        shadow_cost_index=impacts["cost"]["shadow_cost_index"], api_key=api_key
    )

    scenario_report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "tool": "ShadowCost Urban Impact Intelligence",
        "location": display_name,
        "coordinates": {"lat": center_lat, "lon": center_lon},
        "intervention": impacts["intervention_name"],
        "geometry_type": gem_type or "None",
        "dimension": impacts["dimension_val"],
        "metrics": {
            "people_affected": impacts["people_affected"],
            "additional_travel_pct": impacts["additional_travel_pct"],
            "green_area_ha": impacts["green_area_ha"],
            "affected_assets": impacts["affected_assets_count"],
            "shadow_cost_index": impacts["cost"]["shadow_cost_index"]
        },
        "assumptions": {
            "radius_km": radius_km,
            "road_width_m": road_width,
            "detour_factor": detour_factor,
            "demo_seed": int(demo_seed)
        },
        "ai_impact_brief": ai_memo
    }

    # 3 Professional Export Cards matching Phase 1 C
    e1, e2, e3 = st.columns(3)

    with e1:
        st.markdown(
            '<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:12px;padding:1.1rem;margin-bottom:0.75rem;">'
            '<div style="font-family:\'Space Mono\',monospace;font-size:0.7rem;color:#0F766E;font-weight:700;">JSON</div>'
            '<div style="font-weight:700;font-size:0.95rem;color:#111111;margin-top:0.2rem;">SCENARIO DATA</div>'
            '<div style="font-size:0.8rem;color:#4B5563;margin-top:0.25rem;margin-bottom:0.85rem;">Complete machine-readable scenario data</div>'
            '</div>',
            unsafe_allow_html=True
        )
        st.download_button(
            "↓ Download JSON",
            data=json.dumps(scenario_report, indent=2),
            file_name="shadowcost_scenario.json",
            mime="application/json",
            use_container_width=True
        )

    with e2:
        st.markdown(
            '<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:12px;padding:1.1rem;margin-bottom:0.75rem;">'
            '<div style="font-family:\'Space Mono\',monospace;font-size:0.7rem;color:#0F766E;font-weight:700;">CSV</div>'
            '<div style="font-weight:700;font-size:0.95rem;color:#111111;margin-top:0.2rem;">IMPACT SUMMARY</div>'
            '<div style="font-size:0.8rem;color:#4B5563;margin-top:0.25rem;margin-bottom:0.85rem;">Metrics for analysis and spreadsheet reporting</div>'
            '</div>',
            unsafe_allow_html=True
        )
        csv_df = pd.DataFrame([{
            "timestamp": scenario_report["generated_at"],
            "location": display_name,
            "intervention": impacts["intervention_name"],
            "dimensions": impacts["dimension_val"],
            "people_affected": impacts["people_affected"],
            "green_area_ha": impacts["green_area_ha"],
            "travel_pct": impacts["additional_travel_pct"],
            "shadow_cost_index": impacts["cost"]["shadow_cost_index"]
        }])
        st.download_button(
            "↓ Download CSV",
            data=csv_df.to_csv(index=False),
            file_name="shadowcost_scenario.csv",
            mime="text/csv",
            use_container_width=True
        )

    with e3:
        st.markdown(
            '<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:12px;padding:1.1rem;margin-bottom:0.75rem;">'
            '<div style="font-family:\'Space Mono\',monospace;font-size:0.7rem;color:#0F766E;font-weight:700;">REPORT</div>'
            '<div style="font-weight:700;font-size:0.95rem;color:#111111;margin-top:0.2rem;">EXECUTIVE BRIEF</div>'
            '<div style="font-size:0.8rem;color:#4B5563;margin-top:0.25rem;margin-bottom:0.85rem;">Decision-ready executive summary</div>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("Generate Brief", use_container_width=True):
            st.session_state["show_brief"] = True

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    # Expander for Executive Briefing Note (Not expanded by default)
    with st.expander("Preview Executive Brief ▾", expanded=st.session_state.get("show_brief", False)):
        st.markdown(f"""
### Executive Briefing Note: {impacts['intervention_name']}
* **Location:** {display_name}
* **Timestamp:** {scenario_report['generated_at']}
* **Dimension:** {impacts['dimension_val']}
* **Est. Shadow Cost Index:** **{impacts['cost']['shadow_cost_index']} / 100**

#### Key Impact Metrics:
1. **People Affected:** {impacts['people_affected_str']} residents in exposure zone
2. **Mobility Change:** {impacts['additional_travel_str']} travel delay
3. **Green Area Affected:** {impacts['green_area_str']} canopy loss
4. **Affected Assets:** {impacts['affected_assets_str']} structures intersecting corridor

#### AI Impact Brief:
> {ai_memo}
        """)
