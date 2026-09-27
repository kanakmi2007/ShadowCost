"""
core/scenario_manager.py - Scenario Storage & Neutral Trade-Off Comparison Engine
"""

import streamlit as st


def init_scenario_state():
    """Ensure session_state dict for saved scenarios exists."""
    if "scenarios" not in st.session_state:
        st.session_state["scenarios"] = {
            "A": None,
            "B": None
        }


def save_scenario(slot: str, impact_data: dict, scenario_label: str = None):
    """Save active scenario data into slot A or B."""
    init_scenario_state()
    if slot in ["A", "B"]:
        copy_data = dict(impact_data)
        copy_data["slot_label"] = scenario_label or f"Scenario {slot}"
        st.session_state["scenarios"][slot] = copy_data
        return True
    return False


def get_scenarios():
    """Retrieve saved scenarios dict."""
    init_scenario_state()
    return st.session_state["scenarios"]


def generate_comparison_matrix():
    """
    Compares Scenario A and Scenario B.
    Returns structured comparative table and trade-off summary without biased judgment.
    """
    scenarios = get_scenarios()
    scen_a = scenarios.get("A")
    scen_b = scenarios.get("B")

    if not scen_a or not scen_b:
        return None

    # People affected
    pop_a = scen_a.get("people_affected", 0)
    pop_b = scen_b.get("people_affected", 0)
    better_pop = "✓ B" if pop_b < pop_a else ("✓ A" if pop_a < pop_b else "Same")

    # Green area
    green_a = scen_a.get("green_area_ha", 0.0)
    green_b = scen_b.get("green_area_ha", 0.0)
    better_green = "✓ B" if green_b < green_a else ("✓ A" if green_a < green_b else "Same")

    # Peak travel change
    travel_a = scen_a.get("additional_travel_pct", 0.0)
    travel_b = scen_b.get("additional_travel_pct", 0.0)
    better_travel = "✓ B" if travel_b < travel_a else ("✓ A" if travel_a < travel_b else "Same")

    # Shadow cost index
    idx_a = scen_a.get("cost", {}).get("shadow_cost_index", 50)
    idx_b = scen_b.get("cost", {}).get("shadow_cost_index", 50)
    better_idx = "✓ B" if idx_b < idx_a else ("✓ A" if idx_a < idx_b else "Same")

    # Trade-off summary sentence
    if idx_b < idx_a:
        summary_text = (
            f"Scenario B reduces modeled social exposure and green area loss compared to Scenario A, "
            f"offering a lower overall Shadow Cost Index ({idx_b} vs {idx_a})."
        )
    elif idx_a < idx_b:
        summary_text = (
            f"Scenario A reduces modeled social exposure and green area loss compared to Scenario B, "
            f"offering a lower overall Shadow Cost Index ({idx_a} vs {idx_b})."
        )
    else:
        summary_text = "Both alignments carry balanced trade-offs across social, environmental, and mobility lenses."

    return {
        "scenario_a": scen_a,
        "scenario_b": scen_b,
        "rows": [
            {"metric": "People affected", "val_a": f"{pop_a:,}", "val_b": f"{pop_b:,}", "better": better_pop},
            {"metric": "Green area affected", "val_a": f"{green_a:.1f} ha", "val_b": f"{green_b:.1f} ha", "better": better_green},
            {"metric": "Added peak travel", "val_a": f"+{travel_a:.0f}%", "val_b": f"+{travel_b:.0f}%", "better": better_travel},
            {"metric": "Est. shadow cost index", "val_a": f"{idx_a}", "val_b": f"{idx_b}", "better": better_idx},
        ],
        "summary_text": summary_text
    }
