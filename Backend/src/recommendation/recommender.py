
import json

RESOURCES_PATH = "data/skills/learning_resources.json"

def load_resources():
    with open(RESOURCES_PATH, "r") as f:
        return json.load(f)


def recommend_learning(gap_result: dict, resources: dict, max_items=5):
    recommendations = []

    for skill in gap_result["missing"] + gap_result["weak"]:
        if skill in resources:
            recommendations.append({
                "skill": skill,
                "resources": resources[skill]
            })

        if len(recommendations) >= max_items:
            break

    return recommendations
