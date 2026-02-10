def match_resume_to_job(resume_skills: dict, job_skills: dict):
    """
    resume_skills: {skill: confidence (0–1)}
    job_skills: {skill: weight (0–1)}
    """

    score_sum = 0.0
    total_weight = sum(job_skills.values())

    matched = []
    weak = []
    missing = []

    for skill, weight in job_skills.items():
        conf = resume_skills.get(skill, 0.0)

        score_sum += weight * conf

        if conf >= 0.7:
            matched.append(skill)
        elif conf >= 0.3:
            weak.append(skill)
        else:
            missing.append(skill)

    if total_weight == 0:
        fit_score = 0
    else:
        fit_score = round((score_sum / total_weight) * 100, 2)

    # UX safety floor
    fit_score = max(10, fit_score)

    return {
        "fit_score": fit_score,
        "matched": matched,
        "weak": weak,
        "missing": missing
    }
