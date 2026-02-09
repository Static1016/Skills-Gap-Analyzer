def match_resume_to_job(resume_skills, job_skills):
    """
    resume_skills: dict[str, float]  # confidence 0–1
    job_skills: dict[str, float]     # importance weight 0–1
    """

    matched = []
    missing = []

    score_sum = 0.0
    total_weight = sum(job_skills.values()) or 1.0

    for skill, weight in job_skills.items():
        proficiency = resume_skills.get(skill, 0.0)

        if proficiency > 0:
            matched.append(skill)
            score_sum += proficiency * weight
        else:
            missing.append(skill)

    fit_score = round((score_sum / total_weight) * 100, 2)

    return {
        "fit_score": fit_score,
        "matched_skills": matched,
        "missing_skills": missing
    }
