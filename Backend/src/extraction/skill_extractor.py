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


def extract_skills(text: str, skills: list):
    text = normalize_text(text)

    rule = extract_skills_rule_based(text, skills)
    embed = extract_skills_embedding_based(text, skills)

    combined = {}
    for s in set(rule) | set(embed):
        combined[s] = max(rule.get(s, 0), embed.get(s, 0))

    return combined
