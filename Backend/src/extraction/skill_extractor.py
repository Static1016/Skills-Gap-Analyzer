from sentence_transformers import SentenceTransformer, util
import numpy as np

# Load embedding model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def normalize_text(text: str) -> str:
    return " ".join(text.lower().split())


def extract_skills_rule_based(tokens, skills_dict):
    """
    Detects skills using substring matching.
    Works for multi-word skills.
    """
    scores = {}
    joined_text = " ".join(tokens)

    for skill in skills_dict:
        skill_lower = skill.lower()
        if skill_lower in joined_text:
            scores[skill_lower] = 1.0

    return scores


def extract_skills_embedding_based(text, skills_dict, threshold=0.45):
    """
    Uses sentence embeddings to detect semantically similar skills.
    """
    scores = {}

    if not text.strip():
        return scores

    text_embedding = embedding_model.encode(text, convert_to_tensor=True)

    for skill in skills_dict:
        skill_lower = skill.lower()
        skill_embedding = embedding_model.encode(
            skill_lower, convert_to_tensor=True
        )

        similarity = util.cos_sim(text_embedding, skill_embedding).item()

        if similarity >= threshold:
            scores[skill_lower] = round(float(similarity), 2)

    return scores


def combine_skill_scores(rule_scores, embed_scores):
    combined = {}

    for skill in set(rule_scores) | set(embed_scores):
        # rule-based = strong signal
        if skill in rule_scores:
            combined[skill] = 1.0
        else:
            # embedding-based = soft signal
            combined[skill] = embed_scores.get(skill, 0.0)

    return combined


def extract_skills(text, skills_dict):
    """
    Unified skill extraction pipeline.
    """
    text = normalize_text(text)
    tokens = text.split()

    rule_scores = extract_skills_rule_based(tokens, skills_dict)
    embed_scores = extract_skills_embedding_based(text, skills_dict)

    return combine_skill_scores(rule_scores, embed_scores)
