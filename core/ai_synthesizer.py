"""
core/ai_synthesizer.py - OpenAI Policy Synthesis Briefing Engine
"""

import os


def call_ai_synthesis(
    city_name: str,
    intervention_type: str,
    dimension_str: str,
    demolished_summary: str,
    travel_impact_str: str,
    people_affected_str: str,
    green_area_str: str,
    land_overwrite_str: str,
    shadow_cost_index: int = 50,
    api_key: str = None
) -> str:
    """
    Generates a concise, highly professional AI Impact Brief structured around
    the dominant modeled impacts, key considerations, and potential mitigation strategies.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY")

    fallback = (
        f"The dominant modeled impact of this {intervention_type.lower()} in {city_name} is a {travel_impact_str} "
        f"change in peak travel for roughly {people_affected_str} residents, alongside the loss of ~{green_area_str} of green cover. "
        f"Social exposure is concentrated near community structures along the right-of-way. "
        f"Consider a narrower alignment or a preserved green buffer to reduce canopy loss while retaining mobility gains."
    )

    if not key:
        return fallback

    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)

        prompt = (
            f"Location: {city_name}\n"
            f"Intervention: {intervention_type} ({dimension_str})\n"
            f"People Affected: {people_affected_str}\n"
            f"Green Area Loss: {green_area_str}\n"
            f"Travel Impact: {travel_impact_str}\n"
            f"Affected Assets: {demolished_summary}\n"
            f"Est. Shadow Cost Index: {shadow_cost_index}/100\n\n"
            "Write a concise AI Impact Brief of 3 short sentences:\n"
            "Sentence 1 (Summary): Dominant modeled impact on travel and residents.\n"
            "Sentence 2 (Key Considerations): Concentration of social exposure and green cover loss.\n"
            "Sentence 3 (Potential Mitigation): Practical mitigation suggestion (e.g. alignment narrowing, green buffer, rerouting).\n"
            "Keep the language objective, analytical, and framed as modeled decision-support estimates."
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a senior spatial planner providing decision-support policy briefs for infrastructure scenarios."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=220
        )
        return response.choices[0].message.content.strip()

    except Exception:
        return fallback
