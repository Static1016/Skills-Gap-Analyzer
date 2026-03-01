from sentence_transformers import SentenceTransformer, util
import re

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Aliases: maps variations -> canonical skill name (must match job_roles.json keys)
SKILL_ALIASES = {
    "js": "javascript",
    "ts": "typescript",
    "node": "node.js",
    "nodejs": "node.js",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "rest": "rest api",
    "restful": "rest api",
    "restful api": "rest api",
    "k8s": "kubernetes",
    "gcp": "google cloud",
    "ml": "machine learning",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "oop": "object oriented programming",
    "ci/cd": "ci cd",
    "cicd": "ci cd",
    "react.js": "react",
    "reactjs": "react",
    "vue.js": "vue",
    "vuejs": "vue",
    "next.js": "next.js",
    "nextjs": "next.js",
}

# Skill-specific context windows: look for these keywords NEAR a skill mention
# to boost confidence that the person actually used it (not just listed it)
CONTEXT_BOOST_WORDS = {
    "experience", "built", "developed", "implemented", "used", "worked",
    "designed", "deployed", "created", "managed", "led", "proficient",
    "years", "expertise", "familiar", "knowledge"
}


def normalize_text(text: str) -> str:
    """Lowercase and collapse whitespace, but preserve multi-word phrases."""
    text = text.lower()
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def apply_aliases(text: str) -> str:
    """Replace known aliases with canonical names in the text."""
    for alias, canonical in SKILL_ALIASES.items():
        # Use word boundary matching to avoid partial replacements
        text = re.sub(r'\b' + re.escape(alias) + r'\b', canonical, text)
    return text


def extract_skills_rule_based(text: str, skills: list) -> dict:
    """
    Exact string match on the FULL normalized text (not token list).
    This correctly handles multi-word skills like 'rest api', 'node.js'.
    Returns {skill: score} where score reflects simple presence + context boost.
    """
    found = {}
    for skill in skills:
        skill_lower = skill.lower()
        if re.search(r'\b' + re.escape(skill_lower) + r'\b', text):
            # Check if any context boost words appear within ~100 chars of the skill
            match = re.search(r'\b' + re.escape(skill_lower) + r'\b', text)
            start = max(0, match.start() - 100)
            end = min(len(text), match.end() + 100)
            context_window = text[start:end]
            has_context = any(word in context_window for word in CONTEXT_BOOST_WORDS)

            score = 0.95 if has_context else 0.75
            found[skill_lower] = score
    return found


def extract_skills_embedding_based(text: str, skills: list, threshold=0.55) -> dict:
    """
    Instead of embedding the entire resume (too noisy), we extract sentences
    and find the best-matching sentence for each skill. This is much more precise.
    """
    found = {}

    # Split into sentences for focused comparison
    sentences = re.split(r'[.\n;]', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    if not sentences:
        return found

    sentence_embeddings = embedding_model.encode(sentences, convert_to_tensor=True)

    for skill in skills:
        skill_emb = embedding_model.encode(skill, convert_to_tensor=True)
        sims = util.cos_sim(skill_emb, sentence_embeddings)[0]
        best_sim = float(sims.max())

        if best_sim >= threshold:
            found[skill.lower()] = round(best_sim, 2)

    return found


def combine_skill_scores(rule_scores: dict, embed_scores: dict) -> dict:
    """
    Combine rule-based and embedding scores intelligently:
    - Rule-based match: high confidence, use rule score + embed as signal
    - Embed only: lower confidence, use embed score
    - Both agree: boost confidence
    """
    combined = {}
    all_skills = set(rule_scores) | set(embed_scores)

    for skill in all_skills:
        rule = rule_scores.get(skill)
        embed = embed_scores.get(skill)

        if rule is not None and embed is not None:
            # Both agree → high confidence, blend scores
            score = round(rule * 0.6 + embed * 0.4, 2)
            confidence = 0.95
        elif rule is not None:
            # Only rule-based found it → good confidence
            score = rule
            confidence = 0.80
        else:
            # Only semantic similarity found it → lower confidence
            score = embed
            confidence = 0.60

        combined[skill] = {
            "score": min(score, 1.0),
            "confidence": confidence
        }

    return combined


def extract_skills(text: str, skills: list) -> dict:
    """
    Main entry point.
    Returns:
    {
      "skill_name": {
        "score": float (0–1),    # how strongly present
        "confidence": float (0–1) # how sure we are
      }
    }
    """
    text = normalize_text(text)
    text = apply_aliases(text)  # normalize aliases BEFORE matching

    rule_scores = extract_skills_rule_based(text, skills)
    embed_scores = extract_skills_embedding_based(text, skills)

    return combine_skill_scores(rule_scores, embed_scores)