def match_resume_to_job(resume_skills: dict, role_skills: dict) -> dict:
    """
    Computes a weighted fit score comparing resume skill scores to required role skills.

    Args:
        resume_skills: {skill: score (0-1)} extracted from resume
        role_skills:   {skill: weight (0-1)} from job_roles.json

    Returns:
        fit_score, gaps (missing/weak/strong), per-skill scores
    """
    total_weight = sum(role_skills.values())
    score_sum = 0.0

    missing = []
    weak = []
    strong = []
    skill_scores = {}

    for skill, weight in role_skills.items():
        resume_score = resume_skills.get(skill, 0.0)

        # Weighted contribution to overall score
        contribution = min(resume_score, 1.0) * weight
        score_sum += contribution

        # Per-skill score as % of that skill's max possible contribution
        normalized_pct = round((resume_score / 1.0) * 100, 2)
        skill_scores[skill] = normalized_pct

        # Classify skill gap — thresholds calibrated to embedding score ranges
        if resume_score == 0.0:
            missing.append(skill)
        elif resume_score < 0.70:
            # Score present but below strong threshold
            weak.append(skill)
        else:
            strong.append(skill)

    fit_score = round((score_sum / total_weight) * 100, 2) if total_weight else 0.0

    # Cap at 100 (can exceed if resume has higher scores than role requires)
    fit_score = min(fit_score, 100.0)

    return {
        "fit_score": fit_score,
        "gaps": {
            "missing": missing,
            "weak": weak,
            "strong": strong
        },
        "skill_scores": skill_scores
    }