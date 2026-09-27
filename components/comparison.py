"""
components/comparison.py - Scenario Comparison Component (Teal + Black Theme)
"""

import streamlit as st
from core.scenario_manager import get_scenarios, generate_comparison_matrix


def render_comparison_stage(on_next_callback=None, on_export_callback=None):
    """Renders Scenario Comparison Screen with Empty, Partial, and Full Matrix states."""

    c_head_l, c_head_r = st.columns([2, 1])

    with c_head_l:
        st.markdown(
            '<div style="margin-bottom:1.2rem;">'
            '<div style="font-family:\'Space Mono\',monospace;font-size:0.72rem;color:#0F766E;font-weight:700;letter-spacing:0.06em;">COMPARE SCENARIOS</div>'
            '<h1 style="font-size:2rem;font-weight:800;color:#111111;letter-spacing:-0.03em;margin-top:0.15rem;margin-bottom:0.25rem;">'
            'Scenario comparison'
            '</h1>'
            '<div style="font-size:0.9rem;color:#4B5563;">'
            'Understand the trade-offs between two proposed interventions side-by-side.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with c_head_r:
        if st.button("⬇ Export comparison", use_container_width=True):
            if on_export_callback:
                on_export_callback(6)
            st.rerun()

    scenarios = get_scenarios()
    scen_a = scenarios.get("A")
    scen_b = scenarios.get("B")
    matrix = generate_comparison_matrix()

    # PHASE 1 FIX A: EMPTY STATE WHEN SCENARIOS ARE MISSING
    if not scen_a and not scen_b:
        st.markdown(
            '<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:14px;padding:1.25rem;margin-bottom:1.25rem;">'
            '<div style="font-weight:700;font-size:0.88rem;color:#111111;margin-bottom:0.4rem;">💡 HOW TO COMPARE SCENARIOS</div>'
            '<div style="font-size:0.84rem;color:#0F766E;font-weight:600;">'
            '1. Go to Scenario (Step 2) &nbsp;→&nbsp; 2. Draw plan & click Impact Report &nbsp;→&nbsp; 3. Save to Slot A &nbsp;→&nbsp; 4. Draw second plan & Save to Slot B'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        c_slot_a, c_slot_b = st.columns(2, gap="medium")

        with c_slot_a:
            st.markdown(
                '<div style="background:#FFFFFF;border:2px dashed #CBD5E1;border-radius:14px;padding:1.5rem;text-align:center;">'
                '<div style="font-family:\'Space Mono\',monospace;font-size:0.8rem;color:#4B5563;font-weight:700;">SLOT A</div>'
                '<div style="font-weight:800;font-size:1.1rem;color:#111111;margin-top:0.25rem;">SCENARIO A</div>'
                '<div style="font-size:0.8rem;color:#6B7280;margin-top:0.5rem;margin-bottom:1rem;">+ Add first plan</div>'
                '</div>',
                unsafe_allow_html=True
            )
            if st.button("Start Scenario A →", type="primary", use_container_width=True):
                if on_next_callback:
                    on_next_callback(1)
                st.rerun()

        with c_slot_b:
            st.markdown(
                '<div style="background:#FFFFFF;border:2px dashed #CBD5E1;border-radius:14px;padding:1.5rem;text-align:center;">'
                '<div style="font-family:\'Space Mono\',monospace;font-size:0.8rem;color:#4B5563;font-weight:700;">SLOT B</div>'
                '<div style="font-weight:800;font-size:1.1rem;color:#111111;margin-top:0.25rem;">SCENARIO B</div>'
                '<div style="font-size:0.8rem;color:#6B7280;margin-top:0.5rem;margin-bottom:1rem;">+ Add second plan</div>'
                '</div>',
                unsafe_allow_html=True
            )
            if st.button("Compare another plan →", use_container_width=True):
                if on_next_callback:
                    on_next_callback(1)
                st.rerun()
        return

    # PARTIAL STATE (Only A exists)
    if scen_a and not scen_b:
        c_slot_a, c_slot_b = st.columns(2, gap="medium")

        with c_slot_a:
            st.markdown(
                f'<div style="background:#FFFFFF;border:2px solid #0F766E;border-radius:14px;padding:1.2rem;">'
                f'<div style="font-size:0.75rem;font-weight:700;color:#0F766E;">✓ Scenario A Saved</div>'
                f'<div style="font-weight:800;font-size:1.1rem;color:#111111;margin-top:0.25rem;">{scen_a["intervention_name"]}</div>'
                f'<div style="font-size:0.8rem;color:#6B7280;margin-top:0.25rem;">People affected: {scen_a["people_affected_str"]} · Green loss: {scen_a["green_area_str"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        with c_slot_b:
            st.markdown(
                '<div style="background:#FFFFFF;border:2px dashed #CBD5E1;border-radius:14px;padding:1.2rem;text-align:center;">'
                '<div style="font-weight:700;font-size:0.9rem;color:#111111;">Scenario B is Empty</div>'
                '<div style="font-size:0.8rem;color:#6B7280;margin-top:0.25rem;margin-bottom:0.75rem;">Create a second alignment to generate comparison matrix</div>'
                '</div>',
                unsafe_allow_html=True
            )
            if st.button("Create Scenario B →", type="primary", use_container_width=True):
                if on_next_callback:
                    on_next_callback(1)
                st.rerun()
        return

    # FULL MATRIX (Both A and B exist)
    c_card_a, c_card_b = st.columns(2)

    with c_card_a:
        st.markdown(
            f'<div style="background:#FFFFFF;border:2px solid #0F766E;border-radius:14px;padding:1rem;">'
            f'<div style="font-size:0.75rem;font-weight:700;color:#0F766E;margin-bottom:0.25rem;">✓ Scenario A</div>'
            f'<div style="font-weight:800;font-size:1.05rem;color:#111111;">{scen_a["intervention_name"]}</div>'
            f'<div style="font-size:0.78rem;color:#6B7280;margin-top:0.15rem;">Dimension: {scen_a["dimension_val"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    with c_card_b:
        st.markdown(
            f'<div style="background:#FFFFFF;border:1px solid #CBD5E1;border-radius:14px;padding:1rem;">'
            f'<div style="font-size:0.75rem;font-weight:700;color:#4B5563;margin-bottom:0.25rem;">Scenario B</div>'
            f'<div style="font-weight:800;font-size:1.05rem;color:#111111;">{scen_b["intervention_name"]}</div>'
            f'<div style="font-size:0.78rem;color:#6B7280;margin-top:0.15rem;">Dimension: {scen_b["dimension_val"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    # Comparison Table Matrix
    table_rows_html = ""
    for row in matrix["rows"]:
        metric_name = row["metric"]
        better_badge = f'<span style="background:#CCFBF1;color:#0F766E;font-weight:700;padding:0.15rem 0.45rem;border-radius:4px;font-size:0.75rem;">{row["better"]}</span>' if "✓" in row["better"] else f'<span style="color:#6B7280;">{row["better"]}</span>'

        table_rows_html += f'''
        <tr style="border-bottom:1px solid #F1F5F9;">
            <td style="padding:0.75rem 1rem;color:#111111;font-weight:600;">{metric_name}</td>
            <td style="padding:0.75rem 1rem;text-align:center;color:#4B5563;">{row["val_a"]}</td>
            <td style="padding:0.75rem 1rem;text-align:center;color:#111111;font-weight:700;">{row["val_b"]}</td>
            <td style="padding:0.75rem 1rem;text-align:center;">{better_badge}</td>
        </tr>
        '''

    st.markdown(
        '<table style="width:100%;border-collapse:separate;border-spacing:0;background:#FFFFFF;border:1px solid #E5E7EB;border-radius:12px;overflow:hidden;font-size:0.86rem;margin-bottom:1.1rem;">'
        '<thead>'
        '<tr style="background:#F7F7F5;color:#4B5563;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.05em;border-bottom:1px solid #E5E7EB;">'
        '<th style="padding:0.75rem 1rem;text-align:left;font-weight:700;">Impact metric</th>'
        '<th style="padding:0.75rem 1rem;text-align:center;font-weight:700;">Scenario A</th>'
        '<th style="padding:0.75rem 1rem;text-align:center;font-weight:700;">Scenario B</th>'
        '<th style="padding:0.75rem 1rem;text-align:center;font-weight:700;color:#0F766E;">Better</th>'
        '</tr>'
        '</thead>'
        f'<tbody>{table_rows_html}</tbody>'
        '</table>',
        unsafe_allow_html=True
    )

    # Trade-off summary
    st.markdown(
        f'<div style="background:#CCFBF1;border:1px solid #99F6E4;border-radius:12px;padding:1rem 1.25rem;font-size:0.85rem;color:#0F766E;line-height:1.5;">'
        f'{matrix["summary_text"]}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)

    b_col1, _, _ = st.columns([1.2, 1, 1])
    with b_col1:
        if st.button("How is this modeled? →", use_container_width=True):
            if on_next_callback:
                on_next_callback(4)
            st.rerun()
