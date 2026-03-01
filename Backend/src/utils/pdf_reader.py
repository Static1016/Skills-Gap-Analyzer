import fitz  # PyMuPDF
from fastapi import UploadFile


async def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Accepts a FastAPI UploadFile object, reads bytes, and extracts text.
    Previously this function expected raw bytes — but main.py passes
    an UploadFile, which must be awaited first.
    """
    file_bytes = await file.read()
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text