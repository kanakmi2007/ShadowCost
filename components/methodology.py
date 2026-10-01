"""
components/methodology.py - Methodology & KaTeX Mathematical Specifications (Developer Theme)
Flagship Methodology Stage for ShadowCost
"""

import streamlit as st
from config import SVG_ICONS


def render_methodology_stage(on_start_callback=None):
    """Renders Methodology Screen with KaTeX mathematical formulas and pipeline breakdown."""

    st.markdown(
        f"""
        <div style="margin-bottom:1.25rem;">
            <div style="font-family:'Inter',sans-serif;font-size:0.75rem;color:#10B981;font-weight:700;letter-spacing:0.08em;display:flex;align-items:center;gap:0.4rem;">
                {SVG_ICONS['sparkles']} TRANSPARENT ANALYTICAL ARCHITECTURE
            </div>
            <h1 style="font-family:'Inter',sans-serif;font-size:2.2rem;font-weight:800;color:#FFFFFF;letter-spacing:-0.03em;margin-top:0.15rem;margin-bottom:0.35rem;">
                Methodology & Mathematical Specifications
            </h1>
            <div style="font-size:0.9rem;color:#E5E7EB;max-width:850px;line-height:1.55;">
                ShadowCost turns vector spatial interventions into reproducible multi-lens impact metrics via metric UTM projection and GeoPandas spatial intersection.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Process Flow Bar
    st.markdown(
        """
        <div class="glass-panel" style="padding:0.75rem 1.1rem;font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:#10B981;margin-bottom:1.25rem;">
            LOCATION BOUNDS &nbsp;→&nbsp; OPENSTREETMAP GDF &nbsp;→&nbsp; UTM PROJECTION &nbsp;→&nbsp; VECTOR BUFFER &nbsp;→&nbsp; RADAR SUB-SCORES &nbsp;→&nbsp; AI SYNTHESIS
        </div>
        """,
        unsafe_allow_html=True
    )

    # 4 Pipeline Stage Cards
    p1, p2, p3, p4 = st.columns(4)

    with p1:
        st.markdown(
            """
            <div class="glass-panel" style="height:100%;position:relative;">
                <div style="position:absolute;top:0.8rem;right:0.8rem;font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#10B981;font-weight:700;">01</div>
                <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:0.9rem;color:#FFFFFF;">01 SPATIAL INGEST</div>
                <div style="font-size:0.78rem;color:#E5E7EB;margin-top:0.4rem;line-height:1.5;">
                    Pulls target city boundaries, OpenStreetMap building geometries, network nodes, and canopy layers in EPSG:4326.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with p2:
        st.markdown(
            """
            <div class="glass-panel" style="height:100%;position:relative;">
                <div style="position:absolute;top:0.8rem;right:0.8rem;font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#10B981;font-weight:700;">02</div>
                <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:0.9rem;color:#FFFFFF;">02 UTM PROJECTION</div>
                <div style="font-size:0.78rem;color:#E5E7EB;margin-top:0.4rem;line-height:1.5;">
                    Converts WGS84 coordinates dynamically to local metric UTM CRS for accurate area (m²) and corridor length calculations.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with p3:
        st.markdown(
            """
            <div class="glass-panel" style="height:100%;position:relative;">
                <div style="position:absolute;top:0.8rem;right:0.8rem;font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#10B981;font-weight:700;">03</div>
                <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:0.9rem;color:#FFFFFF;">03 INTERSECTION</div>
                <div style="font-size:0.78rem;color:#E5E7EB;margin-top:0.4rem;line-height:1.5;">
                    Executes polygon/polyline buffer intersections across residential housing, commercial retail, and green canopy polygons.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with p4:
        st.markdown(
            """
            <div class="glass-panel" style="height:100%;position:relative;">
                <div style="position:absolute;top:0.8rem;right:0.8rem;font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#10B981;font-weight:700;">04</div>
                <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:0.9rem;color:#FFFFFF;">04 SYNTHESIS</div>
                <div style="font-size:0.78rem;color:#E5E7EB;margin-top:0.4rem;line-height:1.5;">
                    Maps raw spatial numbers into normalized 0-100 lens sub-scores, composite Shadow Index, and OpenAI GPT-4o briefing note.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    # KaTeX Mathematical Specifications (Native st.latex formatting)
    st.markdown("<h3 style='font-family: Inter, sans-serif;'>📐 Mathematical Specifications</h3>", unsafe_allow_html=True)

    f_c1, f_c2 = st.columns(2)

    with f_c1:
        st.markdown(
            """
            <div class="glass-panel" style="padding:1rem;margin-bottom:1rem;">
                <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:0.88rem;color:#10B981;margin-bottom:0.4rem;">
                    1. Metric Corridor Buffer Formulation
                </div>
            """,
            unsafe_allow_html=True
        )
        st.latex(r"C_{\text{utm}} = \text{Line}_{\text{utm}} \oplus \frac{w}{2}")
        st.latex(r"w \in [10, 50] \quad (\text{corridor width in meters})")
        st.markdown(
            """
                <div style="font-size:0.78rem;color:#E5E7EB;margin-top:0.5rem;">
                    Where <code>w</code> is the corridor width applied to metric UTM projected vector geometries.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with f_c2:
        st.markdown(
            """
            <div class="glass-panel" style="padding:1rem;margin-bottom:1rem;">
                <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:0.88rem;color:#10B981;margin-bottom:0.4rem;">
                    2. Composite Shadow Impact Index Formulation
                </div>
            """,
            unsafe_allow_html=True
        )
        st.latex(r"I = \min\left(100, \; 0.35 \, S_{\text{social}} + 0.25 \, S_{\text{env}} + 0.25 \, S_{\text{mob}} + 0.15 \, S_{\text{infra}}\right)")
        st.latex(r"S_{\text{social}}, S_{\text{env}}, S_{\text{mob}}, S_{\text{infra}} \in [0, 100]")
        st.markdown(
            """
                <div style="font-size:0.78rem;color:#E5E7EB;margin-top:0.5rem;">
                    Composite index weighting social exposure, green canopy loss, trip detour multipliers, and infrastructure assets.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    # Four Lenses Matrix
    st.markdown(
        """
        <div class="glass-panel" style="padding:1rem;margin-bottom:1.25rem;">
            <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:1rem;color:#FFFFFF;margin-bottom:0.5rem;">
                Four Spatial Lenses Specification
            </div>
            <table class="dark-table">
                <thead>
                    <tr>
                        <th>Lens</th>
                        <th>Spatial Feature Inputs</th>
                        <th>Primary Output Metric</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="color:#FF4757;font-weight:700;">Social</td>
                        <td>Residential GDF polygons, housing density, community assets</td>
                        <td class="mono">Displaced residents & route disruptions</td>
                    </tr>
                    <tr>
                        <td style="color:#10B981;font-weight:700;">Environment</td>
                        <td>OSM park geometries, tree canopy polygons, heat island mask</td>
                        <td class="mono">Canopy loss (ha) & heat risk level</td>
                    </tr>
                    <tr>
                        <td style="color:#319795;font-weight:700;">Mobility</td>
                        <td>Road network topology, detour multiplier factor, trip routing</td>
                        <td class="mono">Added travel distance & peak delay %</td>
                    </tr>
                    <tr>
                        <td style="color:#FFA500;font-weight:700;">Infrastructure</td>
                        <td>Commercial & civic structures intersected</td>
                        <td class="mono">Shadow Cost Index (0-100)</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True
    )

    c_btn1, _, _ = st.columns([1.3, 1, 1])
    with c_btn1:
        if st.button("Launch Spatial Analysis →", key="method_launch_btn", type="primary", use_container_width=True):
            if on_start_callback:
                on_start_callback(1)
            st.rerun()
