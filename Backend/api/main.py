from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import json

from src.extraction.skill_extractor import extract_skills
from src.scoring.job_matcher import match_resume_to_job
from src.recommendation.recommender import recommend_learning
from src.utils.pdf_reader import extract_text_from_pdf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load job roles
with open("data/roles/job_roles.json") as f:
    JOB_ROLES = json.load(f)

# Load learning resources
with open("data/skills/learning_resources.json") as f:
    LEARNING_RESOURCES = json.load(f)

@app.post("/analyze-job")
async def analyze_job(
    category: str = Form(...),
    role: str = Form(...),
    resume: UploadFile = Form(...)
):
    resume_text = extract_text_from_pdf(resume)

    role_config = JOB_ROLES[category][role]
    role_skills = {k.lower(): float(v) for k, v in role_config["skills"].items()}
    role_label = role_config.get("label", role)

    resume_skills = extract_skills(resume_text, role_skills.keys())

    result = match_resume_to_job(resume_skills, role_skills)
    print(result["gaps"])
    print(LEARNING_RESOURCES.keys())


    recommendations = recommend_learning(result["gaps"], LEARNING_RESOURCES)

    print("RECOMMENDATIONS:", recommendations)


    return {
        "job_fit_score": result["fit_score"],
        "gaps": result["gaps"],
        "skill_scores": result["skill_scores"],
        "role": role_label,
        "recommendations": recommendations,
    }


@app.get("/job-roles")
def get_job_roles():
    return JOB_ROLES
