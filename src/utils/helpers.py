import os
import re
from pathlib import Path


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def ensure_directory(path: str) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def list_supported_files(directory: str) -> list:
    extensions = {".pdf", ".docx", ".txt", ".md", ".html", ".htm"}
    files = []
    for root, _, filenames in os.walk(directory):
        for f in filenames:
            if Path(f).suffix.lower() in extensions:
                files.append(os.path.join(root, f))
    return files
