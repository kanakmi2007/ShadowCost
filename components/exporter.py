"""
components/exporter.py - Executive Brief & Data Exporter Stage (Developer Theme)
Flagship Exporter Stage for ShadowCost
"""

import json
from datetime import datetime
import pandas as pd
import streamlit as st
from config import SVG_ICONS
from core.geocoding import geocode_city_with_buffer
from core.demographics import generate_demographic_features
from core.impact_engine import parse_drawing_geometry, calculate_impacts
from core.ai_synthesizer import call_ai_synthesis


def render_exporter_stage():
    """Renders Executive Brief Exporter Screen with dark glass cards and payload downloads."""

    st.markdown(
        f"""
        <div style="margin-bottom:1.25rem;">
            <div style="font-family:'Inter',sans-serif;font-size:0.75rem;color:#10B981;font-weight:700;letter-spacing:0.08em;display:flex;align-items:center;gap:0.4rem;">
                {SVG_ICONS['brief']} EXECUTIVE BRIEF EXPORTER
            </div>
            <h1 style="font-family:'Inter',sans-serif;font-size:2.1rem;font-weight:800;color:#FFFFFF;letter-spacing:-0.03em;margin-top:0.15rem;margin-bottom:0.35rem;">
                Download Decision Payloads
            </h1>
            <div style="font-size:0.9rem;color:#E5E7EB;">
                Export complete spatial analysis metrics, JSON vector payloads, and decision-ready Executive Briefings.
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
    api_key = st.session_state.get("openai_api_key", "")

    location_result = geocode_city_with_buffer(current_city, buffer_meters=radius_km * 1000.0)
    if location_result is None:
        st.error("Please select a location in Step 1 first.")
        return

    center_lat, center_lon, buffer_geom, bbox, display_name = location_result
    demographic_gdf = generate_demographic_features(center_lat, center_lon, int(demo_seed))

    map_state = st.session_state.get("intervention_map", {})
    drawn_geom, gem_type = parse_drawing_geometry(map_state)

    impacts = calculate_impacts(
        drawn_geom, gem_type, demographic_gdf,
        road_width=road_width, detour_factor=detour_factor
    )

    ai_memo = call_ai_synthesis(
        current_city, impacts["intervention_name"], impacts["dimension_val"],
        impacts["demolished_summary_str"], impacts["additional_travel_str"],
        impacts["people_affected_str"], impacts["green_area_str"],
        impacts["land_overwrite_desc"],
        shadow_cost_index=impacts["shadow_cost_index"], api_key=api_key
    )

    scenario_report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "platform": "ShadowCost Spatial Intelligence Command Center v2.5",
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
            "shadow_cost_index": impacts["shadow_cost_index"],
            "risk_level": impacts["risk_level"]
        },
        "radar_subscores": {
            "social": impacts["social_score"],
            "environment": impacts["env_score"],
            "mobility": impacts["mobility_score"],
            "infrastructure": impacts["infra_score"]
        },
        "ai_impact_brief": ai_memo
    }

    # 3 Dark Glass Export Cards
    e1, e2, e3 = st.columns(3)

    with e1:
        st.markdown(
            """
            <div class="glass-panel" style="padding:1.1rem;margin-bottom:0.75rem;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#10B981;font-weight:700;">FORMAT: JSON</div>
                <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:0.95rem;color:#FFFFFF;margin-top:0.2rem;">SPATIAL JSON PAYLOAD</div>
                <div style="font-size:0.8rem;color:#E5E7EB;margin-top:0.25rem;margin-bottom:0.85rem;">Machine-readable spatial vector payload</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.download_button(
            "Download JSON Payload",
            data=json.dumps(scenario_report, indent=2),
            file_name="shadowcost_spatial_payload.json",
            mime="application/json",
            use_container_width=True
        )

    with e2:
        st.markdown(
            """
            <div class="glass-panel" style="padding:1.1rem;margin-bottom:0.75rem;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#00D2FF;font-weight:700;">FORMAT: CSV</div>
                <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:0.95rem;color:#FFFFFF;margin-top:0.2rem;">METRIC MATRIX CSV</div>
                <div style="font-size:0.8rem;color:#E5E7EB;margin-top:0.25rem;margin-bottom:0.85rem;">Tabular dataset for GIS spreadsheet tools</div>
            </div>
            """,
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
            "shadow_cost_index": impacts["shadow_cost_index"],
            "risk_level": impacts["risk_level"]
        }])
        st.download_button(
            "Download CSV Matrix",
            data=csv_df.to_csv(index=False),
            file_name="shadowcost_impact_metrics.csv",
            mime="text/csv",
            use_container_width=True
        )

    with e3:
        st.markdown(
            """
            <div class="glass-panel" style="padding:1.1rem;margin-bottom:0.75rem;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#FFA500;font-weight:700;">FORMAT: BRIEF</div>
                <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:0.95rem;color:#FFFFFF;margin-top:0.2rem;">EXECUTIVE BRIEFING NOTE</div>
                <div style="font-size:0.8rem;color:#E5E7EB;margin-top:0.25rem;margin-bottom:0.85rem;">Decision-ready policy memorandum</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Preview Briefing Note", key="export_gen_brief", use_container_width=True):
            st.session_state["show_brief"] = True

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    # Executive Briefing Note Panel
    with st.expander("Executive Briefing Note Preview ▾", expanded=st.session_state.get("show_brief", False)):
        st.markdown(f"""
### Executive Briefing Note: {impacts['intervention_name']}
* **Location Node:** {display_name}
* **Timestamp:** {scenario_report['generated_at']}
* **Dimension Footprint:** {impacts['dimension_val']}
* **Shadow Cost Risk Index:** **{impacts['shadow_cost_index']} / 100 ({impacts['risk_level'].upper()} RISK)**

#### Modeled Impact Metrics:
1. **Social Exposure:** {impacts['people_affected_str']} residents inside right-of-way exposure corridor
2. **Mobility Network:** {impacts['additional_travel_str']} travel delay multiplier across daily trips
3. **Environment:** {impacts['green_area_str']} tree canopy removal
4. **Asset Intersections:** {impacts['affected_assets_str']} structures intersected

#### AI Policy Briefing:
> {ai_memo}
        """)
