def recommend_learning(gap_result, resources):
    recommendations = []

    missing = gap_result.get("missing", [])
    weak = gap_result.get("weak", [])

    for skill in missing + weak:
        if skill in resources:
            recommendations.append({
                "skill": skill,
                "resources": resources[skill]
            })

    return recommendations
