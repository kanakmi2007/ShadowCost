"""
components/landing.py - Landing Command Center Workspace (Deep Midnight Theme)
Flagship Overview Screen for ShadowCost
"""

import streamlit as st
from config import SVG_ICONS


def render_landing_stage(on_start_callback=None):
    """Renders Landing Screen with Hero, Quick Demo Launchers, and Interactive Four Lenses."""

    h_left, h_right = st.columns([1.1, 1.2], gap="large")

    with h_left:
        st.markdown(
            f"""
            <div style="font-family:'Space Grotesk',sans-serif;font-size:0.75rem;color:#10B981;font-weight:700;letter-spacing:0.1em;margin-bottom:0.4rem;display:flex;align-items:center;gap:0.4rem;">
                {SVG_ICONS['sparkles']} URBAN SPATIAL IMPACT INTELLIGENCE
            </div>
            <h1 style="font-family:'Space Grotesk',sans-serif;font-size:clamp(2.1rem, 3.8vw, 2.6rem);font-weight:800;letter-spacing:-0.03em;line-height:1.15;color:#FFFFFF;margin-bottom:0.85rem;">
                See the hidden impact<br><span style="color:#10B981;">before you build.</span>
            </h1>
            <div style="font-size:0.95rem;color:#E5E7EB;line-height:1.55;margin-bottom:1.25rem;max-width:520px;">
                ShadowCost helps urban planners, policymakers, and civic teams quantify the hidden social, environmental, mobility, and infrastructure impact of spatial decisions before ground is broken.
            </div>
            """,
            unsafe_allow_html=True
        )

        btn_c1, btn_c2 = st.columns([1.3, 1.2])
        with btn_c1:
            if st.button("Launch Spatial Analysis →", key="hero_launch_btn", type="primary", use_container_width=True):
                if on_start_callback:
                    on_start_callback(1)
                st.rerun()

        with btn_c2:
            if st.button("Explore Methodology", key="hero_method_btn", use_container_width=True):
                if on_start_callback:
                    on_start_callback(4)
                st.rerun()

        st.markdown(
            """
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#9CA3AF;margin-top:1.1rem;">
                GEOPANDAS INTERSECTION ENGINE • OPENSTREETMAP DARK • AI SYNTHESIS
            </div>
            """,
            unsafe_allow_html=True
        )

    with h_right:
        # Visually impressive product preview card (Dark Navy Palette)
        st.markdown(
            f"""
            <div class="glass-panel" style="padding:1rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">
                    <div style="font-family:'Space Grotesk',sans-serif;font-size:0.72rem;font-weight:700;color:#FFFFFF;letter-spacing:0.05em;display:flex;align-items:center;gap:0.4rem;">
                        {SVG_ICONS['radar']} COMMAND PREVIEW
                    </div>
                    <div class="badge badge-emerald" style="font-size:0.65rem;">
                        DEMO SCENARIO PREVIEW
                    </div>
                </div>
                <div style="display:flex;gap:0.75rem;">
                    <div style="flex:1.4;background:#0B0F17;border:1px solid #1E293B;border-radius:8px;height:200px;position:relative;padding:0.6rem;overflow:hidden;">
                        <div style="font-size:0.65rem;color:#9CA3AF;line-height:1.4;">
                            <span style="color:#10B981;">—</span> Proposed Alignment<br>
                            <span style="color:#00D2FF;">●</span> Residential Exposure<br>
                            <span style="color:#FFA500;">●</span> Infrastructure Intersect
                        </div>
                        <!-- Spatial Vector Wireframe Graphic -->
                        <div style="position:absolute;top:30%;left:10%;width:80%;height:45%;border-top:3px solid #10B981;transform:rotate(18deg);border-radius:8px;background:rgba(16,185,129,0.08);border-bottom:1px dashed #00D2FF;"></div>
                        <div style="position:absolute;top:35%;left:25%;width:9px;height:9px;border-radius:50%;background:#10B981;box-shadow:0 0 8px #10B981;"></div>
                        <div style="position:absolute;top:55%;left:55%;width:9px;height:9px;border-radius:50%;background:#00D2FF;box-shadow:0 0 8px #00D2FF;"></div>
                        <div style="position:absolute;top:65%;left:75%;width:9px;height:9px;border-radius:50%;background:#FFA500;box-shadow:0 0 8px #FFA500;"></div>
                    </div>
                    <div style="flex:1;display:flex;flex-direction:column;gap:0.45rem;">
                        <div style="background:rgba(255,255,255,0.03);border:1px solid #1E293B;border-radius:6px;padding:0.4rem 0.6rem;">
                            <div style="font-family:'Space Grotesk',sans-serif;font-size:0.62rem;color:#9CA3AF;font-weight:700;">PEOPLE AFFECTED</div>
                            <div class="metric-mono" style="font-size:1.2rem !important;">450</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.03);border:1px solid #1E293B;border-radius:6px;padding:0.4rem 0.6rem;">
                            <div style="font-family:'Space Grotesk',sans-serif;font-size:0.62rem;color:#9CA3AF;font-weight:700;">MOBILITY SHIFT</div>
                            <div class="metric-mono" style="font-size:1.2rem !important;color:#00D2FF !important;">+23%</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.03);border:1px solid #1E293B;border-radius:6px;padding:0.4rem 0.6rem;">
                            <div style="font-family:'Space Grotesk',sans-serif;font-size:0.62rem;color:#9CA3AF;font-weight:700;">CANOPY LOSS</div>
                            <div class="metric-mono" style="font-size:1.2rem !important;color:#10B981 !important;">1.4 ha</div>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    # INSTANT DEMO SCENARIO LAUNCHERS
    st.markdown(
        f"""
        <div style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);border-radius:8px;padding:0.85rem 1.25rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.75rem;margin-bottom:1.5rem;">
            <div style="display:flex;align-items:center;gap:0.75rem;">
                {SVG_ICONS['sparkles']}
                <div>
                    <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:0.88rem;color:#10B981;">PRESETS</div>
                    <div style="font-size:0.78rem;color:#E5E7EB;">Instant spatial intervention presets with pre-computed polygon geometries and network graphs.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    d_col1, d_col2 = st.columns(2)
    with d_col1:
        if st.button("Preset 1: Road Alignment — Saket, Delhi", key="preset_saket", use_container_width=True):
            st.session_state["current_city_query"] = "Saket, New Delhi"
            st.session_state["radius_km"] = 1.2
            st.session_state["active_tab_idx"] = 1  # Spatial Analysis
            st.session_state["scenario_substep"] = 1  # Draw intervention
            st.rerun()

    with d_col2:
        if st.button("Preset 2: Building Footprint — Bandra West, Mumbai", key="preset_bandra", use_container_width=True):
            st.session_state["current_city_query"] = "Bandra West, Mumbai"
            st.session_state["radius_km"] = 1.2
            st.session_state["active_tab_idx"] = 1
            st.session_state["scenario_substep"] = 1
            st.rerun()

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    # INTERACTIVE FOUR LENSES CARDS WITH CLEAN SVG MARKS
    st.markdown(
        """
        <div style="margin-bottom:1rem;">
            <div style="font-family:'Space Grotesk',sans-serif;font-size:0.72rem;color:#10B981;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;">
                FOUR SPATIAL LENSES
            </div>
            <h2 style="font-family:'Space Grotesk',sans-serif;font-size:1.5rem;font-weight:800;color:#FFFFFF;margin-top:0.15rem;letter-spacing:-0.02em;">
                Multi-dimensional urban impact evaluation
            </h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    l1, l2, l3, l4 = st.columns(4)

    with l1:
        st.markdown(
            f"""
            <div class="glass-panel" style="min-height:160px;">
                <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
                    {SVG_ICONS['social']}
                    <span style="font-family:'Space Grotesk',sans-serif;font-weight:700;color:#FF4757;font-size:0.85rem;">SOCIAL EXPOSURE</span>
                </div>
                <div style="font-size:0.78rem;color:#E5E7EB;line-height:1.45;">
                    Quantifies displaced residents, housing complex intersections, school/clinic proximity, and community route disruption.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with l2:
        st.markdown(
            f"""
            <div class="glass-panel" style="min-height:160px;">
                <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
                    {SVG_ICONS['environment']}
                    <span style="font-family:'Space Grotesk',sans-serif;font-weight:700;color:#10B981;font-size:0.85rem;">ENVIRONMENT</span>
                </div>
                <div style="font-size:0.78rem;color:#E5E7EB;line-height:1.45;">
                    Measures tree canopy removal (ha), green cover percentage loss, and urban heat island micro-climate exposure.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with l3:
        st.markdown(
            f"""
            <div class="glass-panel" style="min-height:160px;">
                <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
                    {SVG_ICONS['mobility']}
                    <span style="font-family:'Space Grotesk',sans-serif;font-weight:700;color:#00D2FF;font-size:0.85rem;">MOBILITY NETWORK</span>
                </div>
                <div style="font-size:0.78rem;color:#E5E7EB;line-height:1.45;">
                    Calculates average added travel distance, network detour factors, daily trip rerouting, and peak-hour congestion multipliers.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with l4:
        st.markdown(
            f"""
            <div class="glass-panel" style="min-height:160px;">
                <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
                    {SVG_ICONS['infrastructure']}
                    <span style="font-family:'Space Grotesk',sans-serif;font-weight:700;color:#FFA500;font-size:0.85rem;">INFRASTRUCTURE</span>
                </div>
                <div style="font-size:0.78rem;color:#E5E7EB;line-height:1.45;">
                    Computes composite Shadow Impact Index (0-100), asset displacement counts, and rights-of-way cost tradeoffs.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
