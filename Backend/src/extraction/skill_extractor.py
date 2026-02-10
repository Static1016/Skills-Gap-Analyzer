from sentence_transformers import SentenceTransformer, util

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def normalize_text(text: str) -> str:
    return " ".join(text.lower().split())


def extract_skills_rule_based(text: str, skills: list):
    found = {}
    for skill in skills:
        if skill.lower() in text:
            found[skill.lower()] = 1.0
    return found


def extract_skills_embedding_based(text: str, skills: list, threshold=0.45):
    found = {}
    text_emb = embedding_model.encode(text, convert_to_tensor=True)

    for skill in skills:
        skill_emb = embedding_model.encode(skill, convert_to_tensor=True)
        sim = util.cos_sim(text_emb, skill_emb).item()
        if sim >= threshold:
            found[skill.lower()] = round(sim, 2)

    return found

def combine_skill_scores(rule_scores, embed_scores):
    combined = {}

    for skill in set(rule_scores) | set(embed_scores):
        if skill in rule_scores:
            combined[skill] = {
                "score": 1.0,
                "confidence": 0.9
            }
        else:
            score = embed_scores.get(skill, 0.0)
            combined[skill] = {
                "score": round(score, 2),
                "confidence": 0.6
            }

    return combined




def extract_skills(text: str, skills: list):
    """
    Returns:
    {
      "skill": {
        "score": float (0–1),
        "confidence": float (0–1)
      }
    }
    """

    text = normalize_text(text)
    tokens = text.split()

    rule_scores = extract_skills_rule_based(tokens, skills)
    embed_scores = extract_skills_embedding_based(text, skills)

    return combine_skill_scores(rule_scores, embed_scores)


