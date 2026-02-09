from src.preprocessing.pdf_reader import extract_text_from_pdf
from fastapi import FastAPI, UploadFile, File
from src.preprocessing.text_cleaner import clean_text
from src.extraction.skill_extractor import (
    load_skills,
    extract_skills_rule_based,
    extract_skills_embedding_based,
    combine_skill_scores
)
from src.scoring.skill_scorer import (
    detect_skill_gaps,
    job_fit_score,
    ML_ENGINEER_SKILLS
)
from src.recommendation.recommender import (
    load_resources,
    recommend_learning
)

app = FastAPI(title="Skill Gap Analyzer API")

skills_dict = load_skills()
resources_dict = load_resources()

@app.post("/analyze-text")
async def analyze_text(payload: dict):
    """
    payload = {
        "text": "... resume text ..."
    }
    """
    raw_text = payload.get("text", "")
    cleaned = clean_text(raw_text)

    rule_scores = extract_skills_rule_based(cleaned.split(), skills_dict)
    embed_scores = extract_skills_embedding_based(cleaned, skills_dict)
    user_skills = combine_skill_scores(rule_scores, embed_scores)

    gaps = detect_skill_gaps(user_skills, ML_ENGINEER_SKILLS)
    fit = job_fit_score(user_skills, ML_ENGINEER_SKILLS)
    recommendations = recommend_learning(gaps, resources_dict)

    return {
        "job_fit_score": fit,
        "skills": user_skills,
        "gaps": gaps,
        "recommendations": recommendations
    }

@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF resumes supported"}

    file_bytes = await file.read()
    raw_text = extract_text_from_pdf(file_bytes)
    cleaned = clean_text(raw_text)

    rule_scores = extract_skills_rule_based(cleaned.split(), skills_dict)
    embed_scores = extract_skills_embedding_based(cleaned, skills_dict)
    user_skills = combine_skill_scores(rule_scores, embed_scores)

    gaps = detect_skill_gaps(user_skills, ML_ENGINEER_SKILLS)
    fit = job_fit_score(user_skills, ML_ENGINEER_SKILLS)
    recommendations = recommend_learning(gaps, resources_dict)

    return {
        "job_fit_score": fit,
        "skills": user_skills,
        "gaps": gaps,
        "recommendations": recommendations
    }
