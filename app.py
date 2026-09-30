"""
app.py - ShadowCost Urban Impact Intelligence Command Center (Main Application Entrypoint)

Developer-Grade Geospatial Platform inspired by Vercel, Linear, and Mapbox Studio.
"""

import os
import streamlit as st

# Streamlit Page Configuration
st.set_page_config(
    page_title="ShadowCost | Spatial Intelligence Platform",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load Global CSS Theme & Config
from config import CSS_THEME, SVG_ICONS, MISSION_STATEMENT
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
    st.session_state["active_tab_idx"] = 0  # 0: Overview, 1: Spatial Analysis, 2: Command Center, 3: Scenario Lab, 4: Methodology, 5: Executive Brief

if "scenario_substep" not in st.session_state:
    st.session_state["scenario_substep"] = 0  # 0: Location, 1: Intervention, 2: Command Center

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

# Helper Callback for 1-Click Quick Demo Mode
def trigger_quick_demo_mode():
    st.session_state["current_city_query"] = "Saket, New Delhi"
    st.session_state["radius_km"] = 1.2
    st.session_state["road_width"] = 25
    st.session_state["detour_factor"] = 1.35
    demo_drawing = {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [77.2140, 28.5210],
                [77.2180, 28.5245],
                [77.2230, 28.5275]
            ]
        }
    }
    st.session_state["intervention_map"] = {
        "all_drawings": [demo_drawing],
        "last_active_drawing": demo_drawing
    }
    st.session_state["active_tab_idx"] = 2  # Jump straight to Command Center
    st.session_state["scenario_substep"] = 2

# Sidebar for advanced assumptions & API key configuration
with st.sidebar:
    st.markdown("<h3 style='font-family: \"Inter\", sans-serif; font-weight: 600;'>Engine Configuration</h3>", unsafe_allow_html=True)
    st.caption("Geospatial parameters & AI Briefing settings")

    demo_s = st.number_input("Demo seed", min_value=1, max_value=9999, value=int(st.session_state["demo_seed"]), step=1)
    if demo_s != st.session_state["demo_seed"]:
        st.session_state["demo_seed"] = demo_s

    st.markdown("---")
    st.markdown("<strong style='font-size:0.85rem;'>AI Briefing Engine</strong>", unsafe_allow_html=True)
    api_k = st.text_input("OpenAI API key (optional)", type="password", value=os.environ.get("OPENAI_API_KEY", ""))
    if api_k:
        os.environ["OPENAI_API_KEY"] = api_k
        st.session_state["openai_api_key"] = api_k

    st.markdown("---")
    if st.button("Trigger Quick Demo Mode", key="sidebar_quick_demo", type="primary", use_container_width=True):
        trigger_quick_demo_mode()
        st.rerun()

    if st.button("Reset Command State", use_container_width=True):
        st.session_state.pop("intervention_map", None)
        st.rerun()

# =========================================================
# DEVELOPER-GRADE NAVIGATION NAVBAR (Zero Text Emojis)
# =========================================================
TABS = ["Overview", "Spatial Analysis", "Command Center", "Scenario Lab", "Methodology", "Executive Report"]
active_idx = st.session_state["active_tab_idx"]

nav_col1, nav_col2, nav_col3 = st.columns([1.2, 5.4, 1.1], gap="small")

with nav_col1:
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:0.5rem;padding-top:0.25rem;">
            {SVG_ICONS['logo']}
            <span style="font-family:'Inter',sans-serif;font-weight:700;font-size:1.15rem;color:#E8EEF5;letter-spacing:-0.02em;">SHADOWCOST</span>
        </div>
        """,
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
        """
        <div style="display:flex;align-items:center;justify-content:flex-end;padding-top:0.35rem;">
            <span class="nav-status"><span class="pulse-ring"></span> SYSTEM ACTIVE</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height:0.3rem;'></div>", unsafe_allow_html=True)

# Helper Navigation Callbacks
def navigate_to_tab(tab_idx: int):
    st.session_state["active_tab_idx"] = tab_idx

def set_scenario_substep(substep_idx: int):
    st.session_state["active_tab_idx"] = 1  # Spatial Analysis tab
    st.session_state["scenario_substep"] = substep_idx

# =========================================================
# ACTIVE TAB RENDERER
# =========================================================

# TAB 0: OVERVIEW (Landing Command Workspace)
if active_idx == 0:
    def handle_landing_navigation(target_idx):
        if target_idx == 4:
            navigate_to_tab(4)
        else:
            set_scenario_substep(0)
    render_landing_stage(on_start_callback=handle_landing_navigation)

# TAB 1: SPATIAL ANALYSIS (Step-by-Step Drawer Flow)
elif active_idx == 1:
    substep = st.session_state.get("scenario_substep", 0)
    if substep == 0:
        render_location_stage(on_next_callback=lambda s: set_scenario_substep(1))
    elif substep == 1:
        render_setup_stage(on_analyze_callback=lambda s: set_scenario_substep(2))
    else:
        render_dashboard_stage(
            on_compare_callback=lambda s: navigate_to_tab(3),
            on_export_callback=lambda s: navigate_to_tab(5)
        )

# TAB 2: COMMAND CENTER (Direct Impact Dashboard Surface)
elif active_idx == 2:
    render_dashboard_stage(
        on_compare_callback=lambda s: navigate_to_tab(3),
        on_export_callback=lambda s: navigate_to_tab(5)
    )

# TAB 3: SCENARIO LAB (A/B Compare View)
elif active_idx == 3:
    render_comparison_stage(
        on_next_callback=lambda s: set_scenario_substep(0),
        on_export_callback=lambda s: navigate_to_tab(5)
    )

# TAB 4: METHODOLOGY (Technical & Mathematical Specifications)
elif active_idx == 4:
    render_methodology_stage(on_start_callback=lambda s: set_scenario_substep(0))

# TAB 5: EXECUTIVE BRIEF (Payload Exporter)
elif active_idx == 5:
    render_exporter_stage()
