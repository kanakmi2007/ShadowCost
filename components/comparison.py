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
                <div style="background:#0D131C;border:1px solid #38A169;border-radius:6px;padding:1rem;">
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

    lat_a = scen_a.get("center_lat", 28.5241)
    lon_a = scen_a.get("center_lon", 77.2181)
    geom_a = scen_a.get("drawn_geom")
    city_a = scen_a.get("city_name", "Saket, New Delhi")

    lat_b = scen_b.get("center_lat", 28.5241)
    lon_b = scen_b.get("center_lon", 77.2181)
    geom_b = scen_b.get("drawn_geom")
    city_b = scen_b.get("city_name", "Saket, New Delhi")

    with map_a_col:
        st.markdown(
            f"""
            <div style="padding:0.75rem;background:#0D131C;border:1px solid #38A169;border-radius:6px;margin-bottom:0.65rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.35rem;">
                    <span class="badge badge-emerald">SCENARIO A (PLAN)</span>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#48BB78;font-weight:700;">Index: {scen_a.get('cost', {}).get('shadow_cost_index', scen_a.get('shadow_cost_index', 50))}/100</span>
                </div>
                <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:1rem;color:#E8EEF5;">{scen_a.get("intervention_name", "Baseline Plan")}</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#8B97A6;margin-top:2px;">
                    ZONE: <strong style="color:#E8EEF5;">{city_a[:35]}</strong> &bull; Dim: <span style="color:#48BB78;">{scen_a.get("dimension_val", "—")}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        mA = folium.Map(
            location=[lat_a, lon_a], zoom_start=15,
            tiles=OSM_TILES, attr=OSM_ATTR, zoom_control=False
        )
        folium.Element(DARK_TILE_CSS).add_to(mA.get_root().header)

        # Catchment zone bound
        folium.Circle(
            location=[lat_a, lon_a], radius=1200,
            color="#E53E3E", weight=1.5, dash_array="6, 6", fill=False, tooltip=f"Edit Zone: {city_a}"
        ).add_to(mA)

        # Draw intervention area geometry if available
        if geom_a is not None:
            if scen_a.get("is_road", True) and hasattr(geom_a, "coords"):
                coords_a = [(p[1], p[0]) for p in geom_a.coords]
                folium.PolyLine(locations=coords_a, color="#E53E3E", weight=6, opacity=0.95, tooltip="Scenario A Corridor Line").add_to(mA)
                folium.CircleMarker(coords_a[0], radius=5, color="#E53E3E", fill=True, fill_color="#E53E3E").add_to(mA)
                folium.CircleMarker(coords_a[-1], radius=5, color="#E53E3E", fill=True, fill_color="#E53E3E").add_to(mA)
            elif hasattr(geom_a, "__geo_interface__"):
                folium.GeoJson(
                    geom_a.__geo_interface__,
                    style_function=lambda x: {"fillColor": "#E53E3E", "color": "#E53E3E", "weight": 2.5, "fillOpacity": 0.5},
                    tooltip="Scenario A Footprint"
                ).add_to(mA)
        else:
            folium.CircleMarker([lat_a, lon_a], radius=7, color="#E53E3E", fill=True, fill_color="#E53E3E", tooltip="Scenario A Focus").add_to(mA)

        st_folium(mA, key="map_compare_A", width=None, height=360, returned_objects=[])

    with map_b_col:
        st.markdown(
            f"""
            <div style="padding:0.75rem;background:#0D131C;border:1px solid #319795;border-radius:6px;margin-bottom:0.65rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.35rem;">
                    <span class="badge badge-cyan">SCENARIO B (ALT PLAN)</span>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#319795;font-weight:700;">Index: {scen_b.get('cost', {}).get('shadow_cost_index', scen_b.get('shadow_cost_index', 50))}/100</span>
                </div>
                <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:1rem;color:#E8EEF5;">{scen_b.get("intervention_name", "Alternative Plan")}</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#8B97A6;margin-top:2px;">
                    ZONE: <strong style="color:#E8EEF5;">{city_b[:35]}</strong> &bull; Dim: <span style="color:#319795;">{scen_b.get("dimension_val", "—")}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        mB = folium.Map(
            location=[lat_b, lon_b], zoom_start=15,
            tiles=OSM_TILES, attr=OSM_ATTR, zoom_control=False
        )
        folium.Element(DARK_TILE_CSS).add_to(mB.get_root().header)

        # Catchment zone bound
        folium.Circle(
            location=[lat_b, lon_b], radius=1200,
            color="#319795", weight=1.5, dash_array="6, 6", fill=False, tooltip=f"Edit Zone: {city_b}"
        ).add_to(mB)

        # Draw intervention area geometry if available
        if geom_b is not None:
            if scen_b.get("is_road", True) and hasattr(geom_b, "coords"):
                coords_b = [(p[1], p[0]) for p in geom_b.coords]
                folium.PolyLine(locations=coords_b, color="#319795", weight=6, opacity=0.95, tooltip="Scenario B Corridor Line").add_to(mB)
                folium.CircleMarker(coords_b[0], radius=5, color="#319795", fill=True, fill_color="#319795").add_to(mB)
                folium.CircleMarker(coords_b[-1], radius=5, color="#319795", fill=True, fill_color="#319795").add_to(mB)
            elif hasattr(geom_b, "__geo_interface__"):
                folium.GeoJson(
                    geom_b.__geo_interface__,
                    style_function=lambda x: {"fillColor": "#319795", "color": "#319795", "weight": 2.5, "fillOpacity": 0.5},
                    tooltip="Scenario B Footprint"
                ).add_to(mB)
        else:
            folium.CircleMarker([lat_b, lon_b], radius=7, color="#319795", fill=True, fill_color="#319795", tooltip="Scenario B Focus").add_to(mB)

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
        <div style="padding:0.85rem;background:#0D131C;border:1px solid rgba(56,161,105,0.25);border-radius:6px;font-size:0.82rem;color:#E8EEF5;line-height:1.55;">
            <div style="font-family:'Inter',sans-serif;font-weight:700;color:#38A169;margin-bottom:0.3rem;">LAB TRADE-OFF SYNTHESIS</div>
            {matrix["summary_text"]}
        </div>
        """,
        unsafe_allow_html=True
    )

