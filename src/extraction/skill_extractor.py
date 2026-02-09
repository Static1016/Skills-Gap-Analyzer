
import json
from pathlib import Path
from collections import defaultdict
from sentence_transformers import SentenceTransformer, util

SKILLS_PATH = "data/skills/skills.json"

# Load SBERT model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_skills():
    with open(SKILLS_PATH, "r") as f:
        return json.load(f)


def extract_skills_rule_based(tokens: list, skills_dict: dict) -> dict:
    skill_freq = defaultdict(int)
    token_text = " ".join(tokens)

    for category, skills in skills_dict.items():
        for skill in skills:
            skill_clean = skill.lower()
            if skill_clean in token_text:
                skill_freq[skill_clean] += token_text.count(skill_clean)

    return dict(skill_freq)


def extract_skills_embedding_based(text: str, skills_dict: dict, threshold=0.6):
    skill_scores = {}

    skill_list = []
    for skills in skills_dict.values():
        skill_list.extend(skills)

    text_embedding = model.encode(text, convert_to_tensor=True)
    skill_embeddings = model.encode(skill_list, convert_to_tensor=True)

    similarities = util.cos_sim(text_embedding, skill_embeddings)[0]

    for skill, score in zip(skill_list, similarities):
        if score >= threshold:
            skill_scores[skill.lower()] = float(score)

    return skill_scores


def combine_skill_scores(rule_scores: dict, embed_scores: dict) -> dict:
    final_scores = {}
    all_skills = set(rule_scores.keys()).union(embed_scores.keys())

    for skill in all_skills:
        freq_score = min(rule_scores.get(skill, 0) / 5, 1.0)
        embed_score = embed_scores.get(skill, 0.0)

        final_scores[skill] = round(
            0.6 * freq_score + 0.4 * embed_score, 3
        )

    return final_scores
