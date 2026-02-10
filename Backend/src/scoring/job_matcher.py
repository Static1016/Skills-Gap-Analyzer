def match_resume_to_job(resume_skills, role_skills):
    """
    resume_skills: { skill: confidence (0–1) }
    role_skills: { skill: weight (0–1) }
    """

    total_weight = sum(role_skills.values())
    if total_weight == 0:
        return {
            "fit_score": 0,
            "gaps": {"missing": [], "weak": [], "strong": []},
            "skill_scores": {}
        }

    score_sum = 0
    skill_scores = {}
    missing = []
    weak = []
    strong = []

    for skill, weight in role_skills.items():
        resume_score = resume_skills.get(skill, 0)

        weighted_score = resume_score * weight
        score_sum += weighted_score

        skill_scores[skill] = round(resume_score * 100, 1)

        if resume_score == 0:
            missing.append(skill)
        elif resume_score < 0.6:
            weak.append(skill)
        else:
            strong.append(skill)

    fit_score = round((score_sum / total_weight) * 100, 1)

    return {
        "fit_score": fit_score,
        "gaps": {
            "missing": missing,
            "weak": weak,
            "strong": strong
        },
        "skill_scores": skill_scores
    }
