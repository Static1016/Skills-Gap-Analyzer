def match_resume_to_job(resume_skills, role_skills):
    total_weight = sum(role_skills.values())
    score_sum = 0.0

    missing = []
    weak = []
    strong = []

    skill_scores = {}

    for skill, weight in role_skills.items():
        resume_score = resume_skills.get(skill, 0)

        # Contribution is capped to role weight
        contribution = min(resume_score, 1.0) * weight
        score_sum += contribution

        normalized = contribution / weight if weight else 0
        skill_scores[skill] = round(normalized * 100, 2)

        if resume_score == 0:
            missing.append(skill)
        elif resume_score < 0.6:
            weak.append(skill)
        else:
            strong.append(skill)

    fit_score = round((score_sum / total_weight) * 100, 2) if total_weight else 0

    return {
        "fit_score": fit_score,
        "gaps": {
            "missing": missing,
            "weak": weak,
            "strong": strong
        },
        "skill_scores": skill_scores
    }
