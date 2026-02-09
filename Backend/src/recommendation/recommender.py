def recommend_learning(gap_result, resources_dict):
    """
    Generates learning recommendations for missing or weak skills.
    Safe against partial gap schemas.
    """

    recommendations = []

    missing = gap_result.get("missing", [])
    weak = gap_result.get("weak", [])

    all_gaps = set(missing + weak)

    for skill in all_gaps:
        skill_lower = skill.lower()

        if skill_lower in resources_dict:
            recommendations.append({
                "skill": skill_lower,
                "resources": resources_dict[skill_lower]
            })

    return recommendations
