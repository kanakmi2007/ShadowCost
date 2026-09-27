"""
app.py - ShadowCost Urban Impact Intelligence (Main Application Entrypoint)

ShadowCost helps planners understand the social, environmental, and mobility
consequences of infrastructure decisions before implementation.
"""

import os
import streamlit as st

# Streamlit Page Configuration
st.set_page_config(
    page_title="ShadowCost | Spatial Intelligence",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load Global CSS Theme
from config import CSS_THEME, MISSION_STATEMENT
st.markdown(CSS_THEME, unsafe_allow_html=True)

# Core Imports
from core.scenario_manager import init_scenario_state

# Component Imports
from components.landing import render_landing_stage
from components.location_selector import render_location_stage
from components.intervention_setup import render_setup_stage
from components.dashboard import render_dashboard_stage
from components.comparison import render_comparison_stage
from components.methodology import render_methodology_stage
from components.exporter import render_exporter_stage

# Initialize Session States
init_scenario_state()

if "active_tab_idx" not in st.session_state:
    st.session_state["active_tab_idx"] = 0  # 0: Overview, 1: Scenario, 2: Impact, 3: Compare, 4: Methodology, 5: Export

if "scenario_substep" not in st.session_state:
    st.session_state["scenario_substep"] = 0  # 0: Location, 1: Intervention, 2: Analysis, 3: Impact

if "current_city_query" not in st.session_state:
    st.session_state["current_city_query"] = "Saket, New Delhi"

if "radius_km" not in st.session_state:
    st.session_state["radius_km"] = 1.2

if "road_width" not in st.session_state:
    st.session_state["road_width"] = 25

if "detour_factor" not in st.session_state:
    st.session_state["detour_factor"] = 1.35

if "demo_seed" not in st.session_state:
    st.session_state["demo_seed"] = 42

# Sidebar for advanced assumptions & API key configuration
with st.sidebar:
    st.markdown("## ⚙️ Scenario Assumptions")
    st.caption("Contextual spatial parameters and API configuration.")

    demo_s = st.number_input("Demo random seed", min_value=1, max_value=9999, value=int(st.session_state["demo_seed"]), step=1)
    if demo_s != st.session_state["demo_seed"]:
        st.session_state["demo_seed"] = demo_s

    st.markdown("---")
    st.markdown("**AI Briefing Configuration**")
    api_k = st.text_input("OpenAI API key (optional)", type="password", value=os.environ.get("OPENAI_API_KEY", ""))
    if api_k:
        os.environ["OPENAI_API_KEY"] = api_k
        st.session_state["openai_api_key"] = api_k

    st.markdown("---")
    if st.button("↺ Reset Scenario State", use_container_width=True):
        st.session_state.pop("intervention_map", None)
        st.rerun()

# =========================================================
# GLOBAL NAVIGATION HEADER (Teal + Black Theme)
# =========================================================
TABS = ["Overview", "Scenario", "Impact", "Compare", "Methodology", "Export"]
active_idx = st.session_state["active_tab_idx"]

nav_col1, nav_col2, nav_col3 = st.columns([1.2, 3.2, 1.1], gap="small")

with nav_col1:
    st.markdown(
        '<div style="font-weight:800;font-size:1.15rem;color:#111111;letter-spacing:-0.02em;display:flex;align-items:center;gap:0.5rem;padding-top:0.2rem;">'
        '<span style="background:#0F766E;color:#FFFFFF;padding:0.15rem 0.5rem;border-radius:6px;font-size:0.85rem;">▲</span> ShadowCost'
        '</div>',
        unsafe_allow_html=True
    )

with nav_col2:
    tab_cols = st.columns(len(TABS))
    for idx, tab_name in enumerate(TABS):
        with tab_cols[idx]:
            btn_kind = "primary" if idx == active_idx else "secondary"
            if st.button(tab_name, key=f"global_tab_{idx}", type=btn_kind, use_container_width=True):
                st.session_state["active_tab_idx"] = idx
                st.rerun()

with nav_col3:
    st.markdown(
        '<div style="display:flex;justify-content:flex-end;align-items:center;gap:0.5rem;padding-top:0.2rem;">'
        '<span style="font-size:0.75rem;font-weight:600;color:#0F766E;background:#CCFBF1;border:1px solid #99F6E4;padding:0.25rem 0.65rem;border-radius:999px;">● Analysis Ready</span>'
        '<span style="background:#111111;color:#FFFFFF;width:28px;height:28px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:0.7rem;font-weight:700;">UP</span>'
        '</div>',
        unsafe_allow_html=True
    )

st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

# Helper Navigation Callbacks
def navigate_to_tab(tab_idx: int):
    st.session_state["active_tab_idx"] = tab_idx

def set_scenario_substep(substep_idx: int):
    st.session_state["active_tab_idx"] = 1  # Scenario tab
    st.session_state["scenario_substep"] = substep_idx

# =========================================================
# ACTIVE TAB RENDERER
# =========================================================

# TAB 0: OVERVIEW (Landing Screen)
if active_idx == 0:
    render_landing_stage(on_start_callback=lambda idx: set_scenario_substep(0))

# TAB 1: SCENARIO WORKSPACE (Location -> Intervention -> Analysis -> Impact)
elif active_idx == 1:
    substep = st.session_state.get("scenario_substep", 0)
    if substep == 0:
        render_location_stage(on_next_callback=lambda s: set_scenario_substep(1))
    elif substep == 1:
        render_setup_stage(on_analyze_callback=lambda s: set_scenario_substep(3))
    else:
        render_dashboard_stage(
            on_compare_callback=lambda s: navigate_to_tab(3),
            on_export_callback=lambda s: navigate_to_tab(5)
        )

# TAB 2: IMPACT REPORT (Direct View)
elif active_idx == 2:
    render_dashboard_stage(
        on_compare_callback=lambda s: navigate_to_tab(3),
        on_export_callback=lambda s: navigate_to_tab(5)
    )

# TAB 3: COMPARE (Scenario Comparison)
elif active_idx == 3:
    render_comparison_stage(
        on_next_callback=lambda s: navigate_to_tab(4),
        on_export_callback=lambda s: navigate_to_tab(5)
    )

# TAB 4: METHODOLOGY (Transparent by design)
elif active_idx == 4:
    render_methodology_stage(on_start_callback=lambda s: set_scenario_substep(0))

# TAB 5: EXPORT (Export Scenario Report)
elif active_idx == 5:
    render_exporter_stage()
