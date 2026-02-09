from src.recommendation.recommender import load_resources, recommend_learning

gap_result = {
    "missing": ["docker", "classification"],
    "weak": ["pandas"],
    "strong": ["python"]
}

resources = load_resources()
recs = recommend_learning(gap_result, resources)

for r in recs:
    print(r)
