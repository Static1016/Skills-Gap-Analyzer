import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Target role profile
ML_ENGINEER_SKILLS = {
    "python": 0.8,
    "numpy": 0.7,
    "pandas": 0.7,
    "scikit-learn": 0.8,
    "linear regression": 0.6,
    "classification": 0.7,
    "clustering": 0.6,
    "docker": 0.6,
    "model deployment": 0.6
}

# Skill gap detection
def detect_skill_gaps(user_skills: dict, role_skills: dict):
    missing = []
    weak = []
    strong = []

    for skill, required_score in role_skills.items():
        user_score = user_skills.get(skill, 0.0)

        if user_score == 0:
            missing.append(skill)
        elif user_score < required_score:
            weak.append(skill)
        else:
            strong.append(skill)

    return {
        "missing": missing,
        "weak": weak,
        "strong": strong
    }

# Job fit score
def job_fit_score(user_skills: dict, role_skills: dict) -> float:
    all_skills = list(role_skills.keys())

    user_vector = np.array(
        [user_skills.get(skill, 0.0) for skill in all_skills]
    ).reshape(1, -1)

    role_vector = np.array(
        [role_skills[skill] for skill in all_skills]
    ).reshape(1, -1)

    score = cosine_similarity(user_vector, role_vector)[0][0]
    return round(score * 100, 2)
