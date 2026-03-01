"""
skill_scorer.py — Standalone utility for testing/debugging skill scores.

This is NOT used by the API. Use it to manually test how the extractor
scores a resume against a role, without running the full server.

Usage:
    python skill_scorer.py
"""

from src.extraction.skill_extractor import extract_skills
from src.scoring.job_matcher import match_resume_to_job

# Example role profile for testing
SAMPLE_ROLE_SKILLS = {
    "node.js": 0.9,
    "express": 0.8,
    "postgresql": 0.8,
    "mongodb": 0.6,
    "rest api": 0.9,
    "jwt": 0.7,
    "authentication": 0.7,
    "aws": 0.6,
    "docker": 0.5,
}

# Paste sample resume text here for quick testing
SAMPLE_RESUME = """
John Doe - Backend Developer
5 years of experience building RESTful APIs with Node.js and Express.
Worked with PostgreSQL and MongoDB for database design.
Deployed applications on AWS using Docker containers.
Implemented JWT-based authentication systems.
"""


def run_test():
    print("=== Skill Extraction Test ===\n")
    skills = extract_skills(SAMPLE_RESUME, list(SAMPLE_ROLE_SKILLS.keys()))

    for skill, data in skills.items():
        print(f"  {skill:25s} score={data['score']:.2f}  confidence={data['confidence']:.2f}")

    print("\n=== Job Match Result ===\n")
    skill_scores = {s: d["score"] for s, d in skills.items()}
    result = match_resume_to_job(skill_scores, SAMPLE_ROLE_SKILLS)

    print(f"  Fit Score : {result['fit_score']}%")
    print(f"  Missing   : {result['gaps']['missing']}")
    print(f"  Weak      : {result['gaps']['weak']}")
    print(f"  Strong    : {result['gaps']['strong']}")


if __name__ == "__main__":
    run_test()