import requests
from bs4 import BeautifulSoup

def extract_job_description(job_input: str) -> str:
    # Case 1: URL
    if job_input.startswith("http"):
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(job_input, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ")
        return " ".join(text.split())

    # Case 2: Pasted job description
    return job_input
