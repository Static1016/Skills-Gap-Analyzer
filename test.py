from src.preprocessing.text_cleaner import preprocess_text

sample = """
I have experience with Python, Pandas, NumPy
and built machine learning models using scikit-learn.
"""

print(preprocess_text(sample))

from pathlib import Path

def load_and_preprocess(file_path: str) -> list:
    text = Path(file_path).read_text(encoding="utf-8")
    return preprocess_text(text)

tokens = load_and_preprocess("data/raw/resumes/resume_1.txt")
print(tokens)