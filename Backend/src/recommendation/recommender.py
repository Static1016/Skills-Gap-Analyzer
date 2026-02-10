def recommend_learning(gaps, resources_dict):
    """
    gaps = {
        "missing": [...],
        "weak": [...]
    }
    resources_dict = {
        "skill": [ {title, url}, ... ]
    }
    """

    recommendations = []

    target_skills = gaps.get("missing", []) + gaps.get("weak", [])

    for skill in target_skills:
        if skill in resources_dict:
            recommendations.append({
                "skill": skill,
                "resources": resources_dict[skill]
            })

    return recommendations
