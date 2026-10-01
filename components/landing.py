"""
components/landing.py - Technical Command Center Landing Page (Phase 1 Dark Spatial Intelligence Theme)
Flagship Spatial Impact Intelligence Workspace for ShadowCost
"""

import streamlit as st
import streamlit.components.v1 as components


def render_landing_stage(on_start_callback=None):
    """Renders Dark Spatial Intelligence Landing Page for ShadowCost."""

    # 1. TOP TECHNICAL HEADER
    st.markdown(
        """
        <div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:1rem;margin-bottom:1.5rem;border-bottom:1px solid rgba(107,114,128,0.15);">
            <div style="display:flex;align-items:center;gap:0.75rem;">
                <span style="font-family:'Inter',sans-serif;font-weight:700;font-size:1.15rem;color:#E8EEF5;letter-spacing:-0.02em;">SHADOWCOST</span>
                <span style="font-family:'Inter',sans-serif;font-size:12px;color:#8B97A6;padding-left:0.75rem;border-left:1px solid rgba(139,151,166,0.15);">Spatial Impact Intelligence Platform</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    # 2. MAIN HERO SECTION (EDITORIAL HIERARCHY)
    h_left, h_right = st.columns([1.05, 1.25], gap="large")

    with h_left:
        st.markdown(
            """
            <div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#38A169;font-weight:600;letter-spacing:0.08em;margin-bottom:0.6rem;display:flex;align-items:center;gap:0.45rem;">
                <span style="display:inline-block;width:6px;height:6px;background:#38A169;border-radius:1px;"></span>
                01 / SPATIAL CONTEXT INTELLIGENCE
            </div>
            <h1 style="font-family:'Inter',sans-serif;font-size:clamp(3rem, 4.5vw, 3.8rem);font-weight:600;letter-spacing:-0.03em;line-height:0.98;color:#E8EEF5;margin-bottom:1.1rem;">
                SEE THE HIDDEN<br>
                <span style="color:#38A169;">IMPACT</span> BEFORE YOU<br>
                BUILD.
            </h1>
            <div style="font-family:'Inter',sans-serif;font-size:15px;color:#8B97A6;line-height:1.55;margin-bottom:1.75rem;max-width:520px;font-weight:400;">
                Understand the social, environmental, mobility, and infrastructure consequences of urban interventions before implementation.
            </div>
            """,
            unsafe_allow_html=True
        )

        btn_c1, btn_c2 = st.columns([1.3, 1.2])
        with btn_c1:
            if st.button("BEGIN ANALYSIS →", key="hero_launch_btn", type="primary", use_container_width=True):
                if on_start_callback:
                    on_start_callback(1)
                st.rerun()

        with btn_c2:
            if st.button("EXPLORE METHODOLOGY", key="hero_method_btn", use_container_width=True):
                if on_start_callback:
                    on_start_callback(4)
                st.rerun()

        st.markdown(
            """
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#6B7280;margin-top:1.5rem;">
                GEOPANDAS INTERSECTION ENGINE &bull; OPENSTREETMAP VECTOR &bull; NETWORK ANALYSIS
            </div>
            """,
            unsafe_allow_html=True
        )

    with h_right:
        # CUMULATIVE SUSTAINABILITY & PLATFORM IMPACT WORKSPACE
        st.markdown(
            """
            <div style="padding:0.75rem;background:#0D131C;border:1px solid rgba(139,151,166,0.12);border-radius:6px;margin-bottom:0.5rem;">
                <div style="font-family:'Inter',sans-serif;font-weight:600;font-size:0.85rem;color:#E8EEF5;margin-bottom:0.4rem;display:flex;align-items:center;justify-content:space-between;">
                    <span>CUMULATIVE SUSTAINABILITY IMPACT TO DATE</span>
                    <span class="badge badge-emerald" style="font-size:10px;">GLOBAL METRICS</span>
                </div>
                <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:0.4rem;margin-bottom:0.6rem;text-align:center;">
                    <div style="background:rgba(255,255,255,0.02);padding:0.4rem 0.2rem;border-radius:4px;border:1px solid rgba(56,161,105,0.2);">
                        <div style="font-size:0.6rem;color:#A0AEC0;font-weight:600;">FOLIAGE SAVED</div>
                        <div style="font-family:'JetBrains Mono',monospace;font-size:0.95rem;font-weight:700;color:#48BB78;margin-top:1px;">148.5 ha</div>
                        <div style="font-size:0.55rem;color:#718096;">~14.8k trees</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.02);padding:0.4rem 0.2rem;border-radius:4px;border:1px solid rgba(49,151,149,0.2);">
                        <div style="font-size:0.6rem;color:#A0AEC0;font-weight:600;">DISPLACEMENT SAVED</div>
                        <div style="font-family:'JetBrains Mono',monospace;font-size:0.95rem;font-weight:700;color:#319795;margin-top:1px;">42.3k</div>
                        <div style="font-size:0.55rem;color:#718096;">residents</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.02);padding:0.4rem 0.2rem;border-radius:4px;border:1px solid rgba(128,90,213,0.2);">
                        <div style="font-size:0.6rem;color:#A0AEC0;font-weight:600;">CO₂ MITIGATED</div>
                        <div style="font-family:'JetBrains Mono',monospace;font-size:0.95rem;font-weight:700;color:#B794F4;margin-top:1px;">21.4k</div>
                        <div style="font-size:0.55rem;color:#718096;">tCO₂e / yr</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.02);padding:0.4rem 0.2rem;border-radius:4px;border:1px solid rgba(221,107,32,0.2);">
                        <div style="font-size:0.6rem;color:#A0AEC0;font-weight:600;">GREEN CORRIDORS</div>
                        <div style="font-family:'JetBrains Mono',monospace;font-size:0.95rem;font-weight:700;color:#DD6B20;margin-top:1px;">58.2 km</div>
                        <div style="font-size:0.55rem;color:#718096;">planned</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        import folium
        from streamlit_folium import st_folium
        from config import DARK_TILE_CSS

        m_cum = folium.Map(
            location=[20.5937, 78.9629],
            zoom_start=4,
            tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            zoom_control=False
        )
        folium.Element(DARK_TILE_CSS).add_to(m_cum.get_root().header)

        # Active Sustainability Nodes Data
        nodes_data = [
            {"lat": 28.5241, "lon": 77.2181, "name": "Saket Node, New Delhi", "foliage": "12.4 ha", "pop": "3,200", "desc": "Green corridor buffer integrated"},
            {"lat": 12.9352, "lon": 77.6245, "name": "Koramangala Node, Bengaluru", "foliage": "18.2 ha", "pop": "4,500", "desc": "Transit spur mobility optimization"},
            {"lat": 19.0600, "lon": 72.8362, "name": "Bandra West Node, Mumbai", "foliage": "14.1 ha", "pop": "5,100", "desc": "Commercial setback preservation"},
            {"lat": 22.5867, "lon": 88.4171, "name": "Salt Lake Node, Kolkata", "foliage": "22.0 ha", "pop": "6,800", "desc": "Eco canopy buffer preserved"},
            {"lat": 40.7128, "lon": -74.0060, "name": "Lower Manhattan, NYC", "foliage": "31.5 ha", "pop": "8,200", "desc": "High-density residential mitigation"},
            {"lat": 51.5074, "lon": -0.1278, "name": "London Transit Corridor", "foliage": "24.8 ha", "pop": "5,900", "desc": "Urban heat island offset zone"}
        ]

        for n in nodes_data:
            folium.Circle(
                location=[n["lat"], n["lon"]],
                radius=45000,
                color="#48BB78",
                weight=1.5,
                fill=True,
                fill_color="#48BB78",
                fill_opacity=0.25,
                tooltip=f"{n['name']} &bull; Foliage Preserved: {n['foliage']}"
            ).add_to(m_cum)
            folium.CircleMarker(
                location=[n["lat"], n["lon"]],
                radius=5,
                color="#2F855A",
                fill=True,
                fill_color="#38A169"
            ).add_to(m_cum)

        st_folium(m_cum, key="cum_sustainability_map", width=None, height=310, returned_objects=[])


    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    # 3. PRE-LOADED SPATIAL PRESETS (DE-BOXED)
    st.markdown(
        """
        <div style="margin-bottom:0.75rem;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;font-weight:700;color:#6B7280;letter-spacing:0.08em;display:flex;align-items:center;gap:0.5rem;">
                <span style="display:inline-block;width:6px;height:6px;background:#0F766E;border-radius:1px;"></span>
                PRE-LOADED SPATIAL PRESETS
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    d_col1, d_col2 = st.columns(2)
    with d_col1:
        if st.button("01  Road Alignment — Saket, Delhi", key="preset_saket", use_container_width=True):
            st.session_state["current_city_query"] = "Saket, New Delhi"
            st.session_state["radius_km"] = 1.2
            st.session_state["active_tab_idx"] = 1
            st.session_state["scenario_substep"] = 1
            st.rerun()

    with d_col2:
        if st.button("02  Building Footprint — Bandra West, Mumbai", key="preset_bandra", use_container_width=True):
            st.session_state["current_city_query"] = "Bandra West, Mumbai"
            st.session_state["radius_km"] = 1.2
            st.session_state["active_tab_idx"] = 1
            st.session_state["scenario_substep"] = 1
            st.rerun()

    st.markdown("<div style='height:1.75rem;'></div>", unsafe_allow_html=True)

    # 4. FOUR SPATIAL LENSES (DE-BOXED EDITORIAL COLUMNS)
    st.markdown(
        """
        <div style="margin-bottom:1.25rem;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#6B7280;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;">
                03 / EVALUATION FRAMEWORK
            </div>
            <h2 style="font-family:'Inter',sans-serif;font-size:1.35rem;font-weight:600;color:#F7F7F5;margin-top:0.2rem;letter-spacing:-0.02em;">
                Four Spatial Lenses for Pre-Implementation Intelligence
            </h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    l1, l2, l3, l4 = st.columns(4)

    with l1:
        st.markdown(
            """
            <div style="border-left:2px solid #0F766E;padding-left:0.75rem;min-height:120px;">
                <div style="font-family:'Inter',sans-serif;font-weight:700;color:#F7F7F5;font-size:0.82rem;margin-bottom:0.4rem;letter-spacing:0.02em;">
                    SOCIAL EXPOSURE
                </div>
                <div style="font-size:0.78rem;color:#9AA4B2;line-height:1.5;">
                    Quantifies displaced residents, housing complex intersections, school/clinic proximity, and community route disruption.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with l2:
        st.markdown(
            """
            <div style="border-left:2px solid #0F766E;padding-left:0.75rem;min-height:120px;">
                <div style="font-family:'Inter',sans-serif;font-weight:700;color:#F7F7F5;font-size:0.82rem;margin-bottom:0.4rem;letter-spacing:0.02em;">
                    ENVIRONMENT
                </div>
                <div style="font-size:0.78rem;color:#9AA4B2;line-height:1.5;">
                    Measures tree canopy removal (ha), green cover percentage loss, and urban heat island micro-climate exposure.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with l3:
        st.markdown(
            """
            <div style="border-left:2px solid #0F766E;padding-left:0.75rem;min-height:120px;">
                <div style="font-family:'Inter',sans-serif;font-weight:700;color:#F7F7F5;font-size:0.82rem;margin-bottom:0.4rem;letter-spacing:0.02em;">
                    MOBILITY NETWORK
                </div>
                <div style="font-size:0.78rem;color:#9AA4B2;line-height:1.5;">
                    Calculates average added travel distance, network detour factors, daily trip rerouting, and peak-hour congestion multipliers.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with l4:
        st.markdown(
            """
            <div style="border-left:2px solid #0F766E;padding-left:0.75rem;min-height:120px;">
                <div style="font-family:'Inter',sans-serif;font-weight:700;color:#F7F7F5;font-size:0.82rem;margin-bottom:0.4rem;letter-spacing:0.02em;">
                    INFRASTRUCTURE
                </div>
                <div style="font-size:0.78rem;color:#9AA4B2;line-height:1.5;">
                    Computes composite Shadow Impact Index (0-100), asset displacement counts, and rights-of-way cost tradeoffs.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:1.75rem;'></div>", unsafe_allow_html=True)

    # 5. TECHNICAL FOOTER
    st.markdown(
        """
        <div style="border-top:1px solid rgba(107,114,128,0.15);padding-top:1rem;margin-top:1rem;display:flex;justify-content:space-between;align-items:center;font-family:'Inter',sans-serif;font-size:0.75rem;color:#6B7280;">
            <div>SHADOWCOST &bull; Urban Spatial Impact Intelligence Platform</div>
        </div>
        """,
        unsafe_allow_html=True
    )

