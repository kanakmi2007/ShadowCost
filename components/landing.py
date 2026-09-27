"""
components/landing.py - Landing Screen Component (Teal + Black Theme)
"""

import streamlit as st


def render_landing_stage(on_start_callback=None):
    """Renders Landing Screen with Hero, Demo Shortcuts, and Interactive Four Lenses."""

    h_left, h_right = st.columns([1.1, 1.2], gap="large")

    with h_left:
        st.markdown(
            '<div style="font-family:\'Space Mono\',monospace;font-size:0.75rem;color:#0F766E;font-weight:700;letter-spacing:0.08em;margin-bottom:0.4rem;">'
            'URBAN IMPACT INTELLIGENCE'
            '</div>'
            '<h1 style="font-size:2.8rem;font-weight:800;letter-spacing:-0.04em;line-height:1.15;color:#111111;margin-bottom:1rem;">'
            'See the hidden impact<br>before you build.'
            '</h1>'
            '<div style="font-size:1.02rem;color:#4B5563;line-height:1.6;margin-bottom:1.5rem;">'
            'ShadowCost helps planners understand the social, environmental and mobility consequences of infrastructure decisions before implementation.'
            '</div>',
            unsafe_allow_html=True
        )

        btn_c1, btn_c2 = st.columns([1.2, 1.2])
        with btn_c1:
            if st.button("Analyze a Scenario →", type="primary", use_container_width=True):
                if on_start_callback:
                    on_start_callback(1)
                st.rerun()

        with btn_c2:
            if st.button("See How It Works", use_container_width=True):
                if on_start_callback:
                    on_start_callback(4)
                st.rerun()

        st.markdown(
            '<div style="font-size:0.8rem;color:#6B7280;margin-top:1.25rem;">'
            'Spatial analysis • Scenario modeling • Decision support'
            '</div>',
            unsafe_allow_html=True
        )

    with h_right:
        # Visually impressive product preview card (Teal + Black palette)
        st.markdown(
            '<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:16px;box-shadow:0 12px 32px -8px rgba(17,17,17,0.06);padding:1.1rem;">'
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.85rem;">'
            '<div style="font-family:\'Space Mono\',monospace;font-size:0.72rem;font-weight:700;color:#0F766E;letter-spacing:0.06em;">PRODUCT PREVIEW — DEMO SCENARIO</div>'
            '<div style="font-size:0.7rem;color:#0F766E;background:#CCFBF1;border:1px solid #99F6E4;padding:0.2rem 0.5rem;border-radius:999px;font-weight:600;">● Active Model</div>'
            '</div>'
            '<div style="display:flex;gap:0.85rem;">'
            '<div style="flex:1.3;background:#F7F7F5;border:1px solid #E5E7EB;border-radius:12px;height:220px;position:relative;padding:0.75rem;overflow:hidden;">'
            '<div style="font-size:0.68rem;color:#4B5563;line-height:1.4;">'
            '<span style="color:#0F766E;">—</span> Proposed Corridor<br>'
            '<span style="color:#2A2A2A;">●</span> Residential Exposure<br>'
            '<span style="color:#14B8A6;">●</span> Canopy Affected'
            '</div>'
            '<div style="position:absolute;top:30%;left:15%;width:70%;height:45%;border-top:3px solid #0F766E;transform:rotate(20deg);border-radius:8px;background:rgba(15,118,110,0.08);border-bottom:1px dashed #6B7280;"></div>'
            '<div style="position:absolute;top:35%;left:25%;width:10px;height:10px;border-radius:50%;background:#111111;"></div>'
            '<div style="position:absolute;top:55%;left:55%;width:10px;height:10px;border-radius:50%;background:#4B5563;"></div>'
            '<div style="position:absolute;top:65%;left:75%;width:10px;height:10px;border-radius:50%;background:#14B8A6;"></div>'
            '</div>'
            '<div style="flex:1;display:flex;flex-direction:column;gap:0.5rem;">'
            '<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:8px;padding:0.5rem 0.75rem;">'
            '<div style="font-size:0.65rem;color:#6B7280;font-weight:700;letter-spacing:0.04em;">PEOPLE AFFECTED</div>'
            '<div style="font-size:1.25rem;font-weight:800;color:#111111;">45</div>'
            '</div>'
            '<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:8px;padding:0.5rem 0.75rem;">'
            '<div style="font-size:0.65rem;color:#6B7280;font-weight:700;letter-spacing:0.04em;">ADDITIONAL TRAVEL</div>'
            '<div style="font-size:1.25rem;font-weight:800;color:#0F766E;">+23%</div>'
            '</div>'
            '<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:8px;padding:0.5rem 0.75rem;">'
            '<div style="font-size:0.65rem;color:#6B7280;font-weight:700;letter-spacing:0.04em;">GREEN AREA</div>'
            '<div style="font-size:1.25rem;font-weight:800;color:#14B8A6;">20.1 ha</div>'
            '</div>'
            '</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    # FEATURE 8 — DEMO MODE SHORTCUTS FOR HACKATHON
    st.markdown(
        '<div style="background:#CCFBF1;border:1px solid #99F6E4;border-radius:12px;padding:0.85rem 1.15rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.75rem;margin-bottom:1.5rem;">'
        '<div>'
        '<div style="font-weight:700;font-size:0.85rem;color:#0F766E;">⚡ Instant Demo Scenarios for Judges</div>'
        '<div style="font-size:0.78rem;color:#115E59;">Load a pre-configured scenario to instantly view spatial analysis & impact reports.</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    d_col1, d_col2 = st.columns(2)
    with d_col1:
        if st.button("🛣️ Try Demo: Road Corridor — Saket", use_container_width=True):
            st.session_state["current_city_query"] = "Saket, New Delhi"
            st.session_state["radius_km"] = 1.2
            st.session_state["active_tab_idx"] = 1  # Scenario tab
            st.session_state["scenario_substep"] = 1  # Intervention setup
            st.rerun()

    with d_col2:
        if st.button("🏗️ Try Demo: Footprint — Bandra West", use_container_width=True):
            st.session_state["current_city_query"] = "Bandra West, Mumbai"
            st.session_state["radius_km"] = 1.2
            st.session_state["active_tab_idx"] = 1
            st.session_state["scenario_substep"] = 1
            st.rerun()

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    # FEATURE 9 — INTERACTIVE FOUR LENSES SECTION
    st.markdown(
        '<div style="margin-bottom:1rem;">'
        '<div style="font-family:\'Space Mono\',monospace;font-size:0.72rem;color:#6B7280;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;">'
        'FOUR LENSES OF HIDDEN IMPACT'
        '</div>'
        '<h2 style="font-size:1.4rem;font-weight:800;color:#111111;margin-top:0.15rem;letter-spacing:-0.02em;">'
        'One decision, measured across what matters'
        '</h2>'
        '</div>',
        unsafe_allow_html=True
    )

    l1, l2, l3, l4 = st.columns(4)

    with l1:
        with st.expander("👥 SOCIAL", expanded=False):
            st.caption("Who is affected?")
            st.markdown("**What ShadowCost measures here:**\nPopulation and community assets inside the exposure zone. Measures displacement, route disruptions, and school/clinic access.")

    with l2:
        with st.expander("🍃 ENVIRONMENT", expanded=False):
            st.caption("What is displaced?")
            st.markdown("**What ShadowCost measures here:**\nTree canopy removed, green cover percentage loss, and localized heat exposure risk.")

    with l3:
        with st.expander("🧭 MOBILITY", expanded=False):
            st.caption("How movement changes?")
            st.markdown("**What ShadowCost measures here:**\nAverage added travel distance, daily trips rerouted, and peak-hour delay multipliers.")

    with l4:
        with st.expander("💲 COST / IMPACT", expanded=False):
            st.caption("Modeled consequences?")
            st.markdown("**What ShadowCost measures here:**\nComposite Shadow Impact Index (0-100) weighting social, environmental, and travel tradeoffs.")

    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)

    # Footer
    st.markdown(
        '<hr style="border-color:#E5E7EB;margin-bottom:1.5rem;">'
        '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;font-size:0.8rem;color:#6B7280;">'
        '<div>'
        '<b style="color:#111111;">ShadowCost</b> &nbsp;·&nbsp; See the hidden impact before you build.'
        '</div>'
        '<div style="font-size:0.75rem;color:#6B7280;">'
        'Prototype · modeled estimates'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )
