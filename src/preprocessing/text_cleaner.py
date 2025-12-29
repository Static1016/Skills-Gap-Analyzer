import re
import spacy

nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def preprocess_text(text: str) -> list:
    #Returns lemmatized token with stopwards removed
    doc = nlp(clean_text(text))
    tokens = [
        token.lemma_
        for token in doc 
        if not token.is_stop and token.is_alpha 
    ]
    return tokens