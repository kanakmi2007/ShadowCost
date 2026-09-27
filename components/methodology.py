"""
components/methodology.py - Methodology Component (Teal + Black Theme)
"""

import streamlit as st


def render_methodology_stage(on_start_callback=None):
    """Renders Methodology Screen with visually connected 4-stage pipeline and expanders."""

    st.markdown(
        '<div style="margin-bottom:1.25rem;">'
        '<div style="font-family:\'Space Mono\',monospace;font-size:0.72rem;color:#0F766E;font-weight:700;letter-spacing:0.06em;">HOW IT WORKS</div>'
        '<h1 style="font-size:2.2rem;font-weight:800;color:#111111;letter-spacing:-0.03em;margin-top:0.15rem;margin-bottom:0.35rem;">'
        'Transparent by design'
        '</h1>'
        '<div style="font-size:0.9rem;color:#4B5563;max-width:850px;line-height:1.55;">'
        'ShadowCost turns a drawn intervention into comparable impact estimates through a four-stage pipeline. Every number is a modeled estimate — meant to inform judgment, not replace it.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # Process Flow Bar
    st.markdown(
        '<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:12px;padding:0.75rem 1.1rem;font-size:0.8rem;color:#0F766E;font-weight:700;margin-bottom:1.25rem;">'
        'LOCATION &nbsp;→&nbsp; URBAN DATA &nbsp;→&nbsp; INTERVENTION &nbsp;→&nbsp; SPATIAL MODEL &nbsp;→&nbsp; IMPACT LENSES &nbsp;→&nbsp; SCENARIO DECISION'
        '</div>',
        unsafe_allow_html=True
    )

    # 4 Pipeline Stage Cards matching Phase 1 B
    p1, p2, p3, p4 = st.columns(4)

    with p1:
        st.markdown(
            '<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:12px;padding:1.1rem;height:100%;position:relative;">'
            '<div style="position:absolute;top:0.8rem;right:0.8rem;font-family:\'Space Mono\',monospace;font-size:0.75rem;color:#0F766E;font-weight:700;">01</div>'
            '<div style="font-weight:700;font-size:0.9rem;color:#111111;margin-top:0.2rem;">01 INPUT</div>'
            '<div style="font-size:0.78rem;color:#4B5563;margin-top:0.4rem;line-height:1.5;">'
            '<b>WHAT GOES IN:</b> Target location & catchment radius.<br>'
            '<b>WHAT HAPPENS:</b> Pulls street network & urban features from open geospatial sources.<br>'
            '<b>WHAT COMES OUT:</b> 2km spatial fabric overlay.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with p2:
        st.markdown(
            '<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:12px;padding:1.1rem;height:100%;position:relative;">'
            '<div style="position:absolute;top:0.8rem;right:0.8rem;font-family:\'Space Mono\',monospace;font-size:0.75rem;color:#0F766E;font-weight:700;">02</div>'
            '<div style="font-weight:700;font-size:0.9rem;color:#111111;margin-top:0.2rem;">02 SPATIAL MODEL</div>'
            '<div style="font-size:0.78rem;color:#4B5563;margin-top:0.4rem;line-height:1.5;">'
            '<b>WHAT GOES IN:</b> Drawn Line/Polygon & corridor width.<br>'
            '<b>WHAT HAPPENS:</b> Projects EPSG:4326 to metric UTM & calculates spatial intersection.<br>'
            '<b>WHAT COMES OUT:</b> Intersecting building & canopy mask.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with p3:
        st.markdown(
            '<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:12px;padding:1.1rem;height:100%;position:relative;">'
            '<div style="position:absolute;top:0.8rem;right:0.8rem;font-family:\'Space Mono\',monospace;font-size:0.75rem;color:#0F766E;font-weight:700;">03</div>'
            '<div style="font-weight:700;font-size:0.9rem;color:#111111;margin-top:0.2rem;">03 IMPACT ANALYSIS</div>'
            '<div style="font-size:0.78rem;color:#4B5563;margin-top:0.4rem;line-height:1.5;">'
            '<b>WHAT GOES IN:</b> Intersected asset features.<br>'
            '<b>WHAT HAPPENS:</b> Evaluates exposure, canopy loss ha, detour multipliers.<br>'
            '<b>WHAT COMES OUT:</b> 4 KPI metrics & 0-100 Index.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with p4:
        st.markdown(
            '<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:12px;padding:1.1rem;height:100%;position:relative;">'
            '<div style="position:absolute;top:0.8rem;right:0.8rem;font-family:\'Space Mono\',monospace;font-size:0.75rem;color:#0F766E;font-weight:700;">04</div>'
            '<div style="font-weight:700;font-size:0.9rem;color:#111111;margin-top:0.2rem;">04 DECISION SUPPORT</div>'
            '<div style="font-size:0.78rem;color:#4B5563;margin-top:0.4rem;line-height:1.5;">'
            '<b>WHAT GOES IN:</b> Quantified impact scores.<br>'
            '<b>WHAT HAPPENS:</b> OpenAI GPT-4o policy synthesis & scenario A/B comparison.<br>'
            '<b>WHAT COMES OUT:</b> Executive Brief & export payload.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    # Technical Details inside Expanders (no screen overwhelm)
    with st.expander("🔬 Technical Formulas & GeoPandas Projection Details", expanded=False):
        st.markdown("""
- **Coordinate Projection:** Coordinates drawn on WGS84 (`EPSG:4326`) are converted dynamically to local metric UTM projections via `GeoPandas.estimate_utm_crs()`.
- **Corridor Buffer:** Road corridors use metric buffer equation: `Corridor_UTM = Line_UTM.buffer(width / 2.0)`.
- **Spatial Intersection:** Building and canopy assets are masked via `demographic_utm.geometry.intersects(corridor_utm)`.
- **Shadow Cost Index:** Composite 0–100 score weighted across exposure density, green canopy loss, and trip detour factors.
        """)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    # The four lenses Table matching Mockup 5
    st.markdown(
        '<div style="font-weight:800;font-size:1.1rem;color:#111111;margin-bottom:0.75rem;">'
        'The four lenses'
        '</div>'
        '<table style="width:100%;border-collapse:separate;border-spacing:0;background:#FFFFFF;border:1px solid #E5E7EB;border-radius:12px;overflow:hidden;font-size:0.85rem;margin-bottom:1.25rem;">'
        '<thead>'
        '<tr style="background:#F7F7F5;color:#4B5563;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.05em;border-bottom:1px solid #E5E7EB;">'
        '<th style="padding:0.75rem 1rem;text-align:left;font-weight:700;">Lens</th>'
        '<th style="padding:0.75rem 1rem;text-align:left;font-weight:700;">Key Inputs</th>'
        '<th style="padding:0.75rem 1rem;text-align:left;font-weight:700;">Primary output</th>'
        '</tr>'
        '</thead>'
        '<tbody>'
        '<tr style="border-bottom:1px solid #F1F5F9;">'
        '<td style="padding:0.85rem 1rem;font-weight:700;color:#111111;">👥 Social</td>'
        '<td style="padding:0.85rem 1rem;color:#4B5563;">Population density, community assets, pedestrian routes</td>'
        '<td style="padding:0.85rem 1rem;color:#111111;font-weight:600;">People within exposure zone</td>'
        '</tr>'
        '<tr style="border-bottom:1px solid #F1F5F9;">'
        '<td style="padding:0.85rem 1rem;font-weight:700;color:#111111;">🍃 Environmental</td>'
        '<td style="padding:0.85rem 1rem;color:#4B5563;">Tree canopy, green cover, land use</td>'
        '<td style="padding:0.85rem 1rem;color:#111111;font-weight:600;">Displaced green area & heat risk</td>'
        '</tr>'
        '<tr style="border-bottom:1px solid #F1F5F9;">'
        '<td style="padding:0.85rem 1rem;font-weight:700;color:#111111;">🧭 Mobility</td>'
        '<td style="padding:0.85rem 1rem;color:#4B5563;">Network topology, detour factor, trip flows</td>'
        '<td style="padding:0.85rem 1rem;color:#111111;font-weight:600;">Added travel distance & delay</td>'
        '</tr>'
        '<tr>'
        '<td style="padding:0.85rem 1rem;font-weight:700;color:#111111;">💲 Cost</td>'
        '<td style="padding:0.85rem 1rem;color:#4B5563;">Weighted composite of the three lenses</td>'
        '<td style="padding:0.85rem 1rem;color:#111111;font-weight:600;">Shadow cost index (0–100)</td>'
        '</tr>'
        '</tbody>'
        '</table>',
        unsafe_allow_html=True
    )

    # Uncertainty Callout Box
    st.markdown(
        '<div style="background:#CCFBF1;border:1px solid #99F6E4;border-radius:12px;padding:0.85rem 1.1rem;font-size:0.82rem;color:#0F766E;margin-bottom:1.25rem;">'
        'ⓘ <b>Estimates carry uncertainty</b> and depend on your assumptions and input data quality. ShadowCost is a decision-support tool; validate critical decisions with field surveys and stakeholder input.'
        '</div>',
        unsafe_allow_html=True
    )

    c_btn1, _, _ = st.columns([1.2, 1, 1])
    with c_btn1:
        if st.button("Analyze a Scenario →", type="primary", use_container_width=True):
            if on_start_callback:
                on_start_callback(1)
            st.rerun()
