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
    resume: UploadFile = File(...)  # Fixed: was Form(...), should be File(...)
):
    # 1. Extract raw text — NOTE: must await since pdf_reader is now async
    resume_text = await extract_text_from_pdf(resume)

    # 2. Load role config
    role_config = JOB_ROLES[category][role]
    role_skills = {
        k.lower(): float(v)
        for k, v in role_config["skills"].items()
    }
    role_label = role_config.get("label", role)

    # 3. Extract skills WITH confidence scores
    resume_skills = extract_skills(resume_text, list(role_skills.keys()))
    # resume_skills = {
    #   "python": {"score": 0.95, "confidence": 0.95},
    #   "rest api": {"score": 0.72, "confidence": 0.80}
    # }

    # 4. Separate score & confidence
    resume_skill_scores = {
        skill: data["score"]
        for skill, data in resume_skills.items()
    }
    resume_skill_confidence = {
        skill: data["confidence"]
        for skill, data in resume_skills.items()
    }

    # 5. Match resume to job role
    result = match_resume_to_job(resume_skill_scores, role_skills)

    # 6. Generate learning recommendations for gaps
    recommendations = recommend_learning(
        result["gaps"],
        LEARNING_RESOURCES
    )

    # 7. Return response
    return {
        "job_fit_score": result["fit_score"],
        "gaps": result["gaps"],
        "skill_scores": result["skill_scores"],
        "confidence": resume_skill_confidence,
        "role": role_label,
        "recommendations": recommendations
    }


@app.post("/analyze-job-with-description")
async def analyze_job_with_description(
    category: str = Form(...),
    role: str = Form(...),
    resume: UploadFile = File(...),
    job_description: str = Form("")
):
    """
    Optional: if job_description is provided, blend role skills with
    skills extracted from the JD for a more tailored analysis.
    """
    resume_text = await extract_text_from_pdf(resume)

    role_config = JOB_ROLES[category][role]
    role_skills = {
        k.lower(): float(v)
        for k, v in role_config["skills"].items()
    }
    role_label = role_config.get("label", role)

    # If JD provided, extract skills from it and merge (JD skills weighted at 0.7 default)
    if job_description.strip():
        jd_skills = extract_skills(job_description, list(role_skills.keys()))
        for skill, data in jd_skills.items():
            if skill not in role_skills:
                role_skills[skill] = 0.7  # add JD-only skills with moderate weight
            # If already in role, slightly boost weight if JD also emphasizes it
            else:
                role_skills[skill] = min(role_skills[skill] * 1.1, 1.0)

    resume_skills = extract_skills(resume_text, list(role_skills.keys()))

    resume_skill_scores = {skill: data["score"] for skill, data in resume_skills.items()}
    resume_skill_confidence = {skill: data["confidence"] for skill, data in resume_skills.items()}

    result = match_resume_to_job(resume_skill_scores, role_skills)
    recommendations = recommend_learning(result["gaps"], LEARNING_RESOURCES)

    return {
        "job_fit_score": result["fit_score"],
        "gaps": result["gaps"],
        "skill_scores": result["skill_scores"],
        "confidence": resume_skill_confidence,
        "role": role_label,
        "recommendations": recommendations,
        "jd_used": bool(job_description.strip())
    }


@app.get("/job-roles")
def get_job_roles():
    return JOB_ROLES