from sentence_transformers import SentenceTransformer, util

# Load embedding model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Tunable constants
RULE_BASED_CONFIDENCE = 0.7   # strong but not perfect
EMBEDDING_MAX_CONFIDENCE = 0.6


def normalize_text(text: str) -> str:
    return " ".join(text.lower().split())


def extract_skills_rule_based(tokens, skills_dict):
    """
    Detects skills using substring matching.
    Assigns strong but non-perfect confidence.
    """
    scores = {}
    joined_text = " ".join(tokens)

    for skill in skills_dict:
        skill_lower = skill.lower()
        if skill_lower in joined_text:
            scores[skill_lower] = RULE_BASED_CONFIDENCE

    return scores


def extract_skills_embedding_based(text, skills_dict, threshold=0.45):
    """
    Uses sentence embeddings to detect semantically similar skills.
    Produces soft confidence scores.
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
            # scale similarity to soft confidence
            scores[skill_lower] = min(
                round(float(similarity), 2),
                EMBEDDING_MAX_CONFIDENCE
            )

    return scores


def combine_skill_scores(rule_scores, embed_scores):
    """
    Combines rule-based and embedding-based signals.
    Rule-based dominates but does NOT saturate to 1.0.
    """
    combined = {}

    for skill in set(rule_scores) | set(embed_scores):
        combined[skill] = max(
            rule_scores.get(skill, 0.0),
            embed_scores.get(skill, 0.0)
        )

    return combined


def extract_skills(text, skills_dict):
    """
    Unified skill extraction pipeline.
    Returns confidence scores in range ~0.3–0.7
    """
    text = normalize_text(text)
    tokens = text.split()

    rule_scores = extract_skills_rule_based(tokens, skills_dict)
    embed_scores = extract_skills_embedding_based(text, skills_dict)

    return combine_skill_scores(rule_scores, embed_scores)
