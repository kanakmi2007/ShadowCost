"""
components/comparison.py - Scenario Lab Dual Map A/B Comparison Stage (Developer Theme)
Flagship Scenario Lab Core for ShadowCost
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
from config import SVG_ICONS, OSM_TILES, OSM_ATTR, DARK_TILE_CSS
from core.scenario_manager import get_scenarios, generate_comparison_matrix


def render_comparison_stage(on_next_callback=None, on_export_callback=None):
    """Renders Scenario Lab Comparison Screen with Dual Side-by-Side Maps & Matrix states."""

    c_head_l, c_head_r = st.columns([2.2, 1])

    with c_head_l:
        st.markdown(
            f"""
            <div style="margin-bottom:1.2rem;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#4A5568;font-weight:600;letter-spacing:0.1em;margin-bottom:0.4rem;">
                    04 / SCENARIO LAB A/B COMPARE
                </div>
                <h1 style="font-family:'Inter',sans-serif;font-size:1.8rem;font-weight:600;color:#E8EEF5;letter-spacing:-0.03em;margin-top:0.1rem;margin-bottom:0.25rem;">
                    Multi-Scenario Trade-off Matrix
                </h1>
                <div style="font-size:0.85rem;color:#8B97A6;">
                    Side-by-side spatial exposure analysis and comparative trade-off matrix.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c_head_r:
        if st.button("Export Lab Report", key="comp_export_btn", type="primary", use_container_width=True):
            if on_export_callback:
                on_export_callback(5)
            st.rerun()

    scenarios = get_scenarios()
    scen_a = scenarios.get("A")
    scen_b = scenarios.get("B")
    matrix = generate_comparison_matrix()

    # EMPTY STATE WHEN NO SCENARIOS SAVED
    if not scen_a and not scen_b:
        st.markdown(
            """
            <div style="padding:0.85rem;background:#0D131C;border:1px solid rgba(139,151,166,0.12);border-radius:6px;margin-bottom:1rem;">
                <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:0.85rem;color:#14B8A6;margin-bottom:0.3rem;">DRAW OR LOAD A SCENARIO TO BEGIN COMPARISON</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#8B97A6;">
                    1. SPATIAL ANALYSIS &nbsp;&rarr;&nbsp; 2. DRAW INTERVENTION &nbsp;&rarr;&nbsp; 3. SAVE TO SLOT A / SLOT B &nbsp;&rarr;&nbsp; 4. VIEW LIVE MATRIX
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        c_slot_a, c_slot_b = st.columns(2, gap="medium")

        with c_slot_a:
            st.markdown(
                """
                <div style="background:#0D131C;border:1px dashed rgba(139,151,166,0.2);border-radius:6px;padding:1.25rem;text-align:center;">
                    <div style="font-family:'Inter',sans-serif;font-size:0.75rem;color:#8B97A6;font-weight:700;">SLOT A</div>
                    <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:1.1rem;color:#E8EEF5;margin-top:0.25rem;">SCENARIO A (BASELINE)</div>
                    <div style="font-size:0.78rem;color:#4A5568;margin-top:0.4rem;margin-bottom:0.85rem;">+ Draw or save primary alignment plan</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("Draw Scenario A →", key="comp_draw_a", type="primary", use_container_width=True):
                if on_next_callback:
                    on_next_callback(1)
                st.rerun()

        with c_slot_b:
            st.markdown(
                """
                <div style="background:#0D131C;border:1px dashed rgba(139,151,166,0.2);border-radius:6px;padding:1.25rem;text-align:center;">
                    <div style="font-family:'Inter',sans-serif;font-size:0.75rem;color:#8B97A6;font-weight:700;">SLOT B</div>
                    <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:1.1rem;color:#E8EEF5;margin-top:0.25rem;">SCENARIO B (ALTERNATIVE)</div>
                    <div style="font-size:0.78rem;color:#4A5568;margin-top:0.4rem;margin-bottom:0.85rem;">+ Draw or save alternative alignment plan</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("Draw Scenario B →", key="comp_draw_b", use_container_width=True):
                if on_next_callback:
                    on_next_callback(1)
                st.rerun()
        return

    # PARTIAL STATE (Only Slot A exists)
    if scen_a and not scen_b:
        c_slot_a, c_slot_b = st.columns(2, gap="medium")

        with c_slot_a:
            st.markdown(
                f"""
                <div style="background:#0D131C;border:1px solid #14B8A6;border-radius:6px;padding:1rem;">
                    <div class="badge badge-emerald" style="margin-bottom:0.4rem;">SCENARIO A SAVED</div>
                    <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:1.1rem;color:#E8EEF5;">{scen_a["intervention_name"]}</div>
                    <div style="font-size:0.78rem;color:#8B97A6;margin-top:0.25rem;">Residents affected: {scen_a["people_affected_str"]} &bull; Canopy: {scen_a["green_area_str"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c_slot_b:
            st.markdown(
                """
                <div style="background:#0D131C;border:1px dashed rgba(139,151,166,0.2);border-radius:6px;padding:1rem;text-align:center;">
                    <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:0.9rem;color:#E8EEF5;">Scenario B is Empty</div>
                    <div style="font-size:0.78rem;color:#4A5568;margin-top:0.25rem;margin-bottom:0.65rem;">Draw an alternative corridor to generate trade-off matrix</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("Create Scenario B →", key="comp_create_b", type="primary", use_container_width=True):
                if on_next_callback:
                    on_next_callback(1)
                st.rerun()
        return

    # FULL MATRIX (Both Slot A and Slot B exist) - DYNAMIC METRIC DELTAS STRIP
    pop_d = scen_b.get("people_affected", 0) - scen_a.get("people_affected", 0)
    pop_d_badge = f'<span class="badge badge-rose">{pop_d:+} residents</span>' if pop_d != 0 else '<span class="badge badge-emerald">0 residents</span>'
    
    travel_d = scen_b.get("additional_travel_pct", 0) - scen_a.get("additional_travel_pct", 0)
    travel_d_badge = f'<span class="badge badge-cyan">{travel_d:+.0f}% travel delay</span>' if travel_d != 0 else '<span class="badge badge-cyan">0% travel delay</span>'

    green_d = scen_b.get("green_area_ha", 0) - scen_a.get("green_area_ha", 0)
    green_d_badge = f'<span class="badge badge-emerald">{green_d:+.1f} ha canopy</span>' if green_d != 0 else '<span class="badge badge-emerald">0 ha canopy</span>'

    st.markdown(
        f"""
        <div style="padding:0.75rem 1rem;background:#0D131C;border:1px solid rgba(139,151,166,0.12);border-radius:6px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.75rem;margin-bottom:1rem;">
            <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:0.8rem;color:#E8EEF5;">DYNAMIC METRIC DELTAS (Slot B vs A):</div>
            <div style="display:flex;gap:0.75rem;">
                {pop_d_badge}
                {travel_d_badge}
                {green_d_badge}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # DUAL SIDE-BY-SIDE INTERACTIVE MAP VIEWS
    map_a_col, map_b_col = st.columns(2, gap="medium")

    with map_a_col:
        st.markdown(
            f"""
            <div style="padding:0.75rem;background:#0D131C;border:1px solid #14B8A6;border-radius:6px;margin-bottom:0.65rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.35rem;">
                    <span class="badge badge-emerald">SCENARIO A MAP</span>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#14B8A6;font-weight:700;">Index: {scen_a.get('cost', {}).get('shadow_cost_index', 50)}/100</span>
                </div>
                <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:1rem;color:#E8EEF5;">{scen_a["intervention_name"]}</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#8B97A6;">Dimension: {scen_a["dimension_val"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        mA = folium.Map(
            location=[28.5241, 77.2181], zoom_start=14,
            tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            zoom_control=False
        )
        folium.Element("""
        <style>
            .leaflet-tile-pane {
                filter: brightness(0.6) invert(1) contrast(3) hue-rotate(200deg) saturate(0.3);
            }
        </style>
        """).add_to(mA.get_root().header)
        st_folium(mA, key="map_compare_A", width=None, height=360, returned_objects=[])

    with map_b_col:
        st.markdown(
            f"""
            <div style="padding:0.75rem;background:#0D131C;border:1px solid #5EEAD4;border-radius:6px;margin-bottom:0.65rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.35rem;">
                    <span class="badge badge-cyan">SCENARIO B MAP</span>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#5EEAD4;font-weight:700;">Index: {scen_b.get('cost', {}).get('shadow_cost_index', 50)}/100</span>
                </div>
                <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:1rem;color:#E8EEF5;">{scen_b["intervention_name"]}</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#8B97A6;">Dimension: {scen_b["dimension_val"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        mB = folium.Map(
            location=[28.5241, 77.2181], zoom_start=14,
            tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            zoom_control=False
        )
        folium.Element("""
        <style>
            .leaflet-tile-pane {
                filter: brightness(0.6) invert(1) contrast(3) hue-rotate(200deg) saturate(0.3);
            }
        </style>
        """).add_to(mB.get_root().header)
        st_folium(mB, key="map_compare_B", width=None, height=360, returned_objects=[])

    st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)

    # Comparison Table Matrix
    table_rows_html = ""
    for row in matrix["rows"]:
        metric_name = row["metric"]
        better_badge = f'<span class="badge badge-emerald">{row["better"]}</span>' if "✓" in row["better"] else f'<span style="color:#8B97A6;">{row["better"]}</span>'

        table_rows_html += f'''
        <tr>
            <td style="color:#E8EEF5;font-weight:600;">{metric_name}</td>
            <td class="mono" style="text-align:center;color:#8B97A6;">{row["val_a"]}</td>
            <td class="mono" style="text-align:center;color:#E8EEF5;font-weight:700;">{row["val_b"]}</td>
            <td style="text-align:center;">{better_badge}</td>
        </tr>
        '''

    st.markdown(
        f"""
        <div style="padding:0.85rem;background:#0D131C;border:1px solid rgba(139,151,166,0.12);border-radius:6px;margin-bottom:1rem;">
            <table class="dark-table">
                <thead>
                    <tr>
                        <th>Impact Metric</th>
                        <th style="text-align:center;">Scenario A</th>
                        <th style="text-align:center;">Scenario B</th>
                        <th style="text-align:center;">Optimal</th>
                    </tr>
                </thead>
                <tbody>{table_rows_html}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Trade-off summary card
    st.markdown(
        f"""
        <div style="padding:0.85rem;background:#0D131C;border:1px solid rgba(20,184,166,0.25);border-radius:6px;font-size:0.82rem;color:#E8EEF5;line-height:1.55;">
            <div style="font-family:'Inter',sans-serif;font-weight:700;color:#14B8A6;margin-bottom:0.3rem;">LAB TRADE-OFF SYNTHESIS</div>
            {matrix["summary_text"]}
        </div>
        """,
        unsafe_allow_html=True
    )
