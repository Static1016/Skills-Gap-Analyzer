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
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Skill Gap Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

skills_dict = load_skills()
resources_dict = load_resources()

from src.roles.role_loader import load_roles, get_role_skills

roles_data = load_roles()


@app.post("/analyze-resume")
async def analyze_resume(
    category: str,
    role: str,
    file: UploadFile = File(...)
):
    file_bytes = await file.read()
    raw_text = extract_text_from_pdf(file_bytes)
    cleaned = clean_text(raw_text)

    rule_scores = extract_skills_rule_based(cleaned.split(), skills_dict)
    embed_scores = extract_skills_embedding_based(cleaned, skills_dict)
    user_skills = combine_skill_scores(rule_scores, embed_scores)

    role_skills = get_role_skills(roles_data, category, role)

    gaps = detect_skill_gaps(user_skills, role_skills)
    fit = job_fit_score(user_skills, role_skills)
    recommendations = recommend_learning(gaps, resources_dict)

    return {
        "role": roles_data[category][role]["label"],
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

@app.get("/job-roles")
def get_job_roles():
    result = {}
    for category, roles in roles_data.items():
        result[category] = {
            key: role["label"]
            for key, role in roles.items()
        }
    return result
