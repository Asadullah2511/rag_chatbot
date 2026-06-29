from pathlib import Path
from typing import List

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    UnstructuredHTMLLoader,
)
from langchain_core.documents import Document


SUPPORTED_EXTENSIONS = {
    ".pdf": PyPDFLoader,
    ".docx": Docx2txtLoader,
    ".txt": TextLoader,
    ".md": TextLoader,
    ".html": UnstructuredHTMLLoader,
    ".htm": UnstructuredHTMLLoader,
}


def load_document(file_path: str) -> List[Document]:
    path = Path(file_path)
    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}. Supported: {list(SUPPORTED_EXTENSIONS.keys())}")
    loader_cls = SUPPORTED_EXTENSIONS[ext]
    loader = loader_cls(str(path))
    return loader.load()


def load_documents_from_directory(directory: str) -> List[Document]:
    all_docs = []
    for ext in SUPPORTED_EXTENSIONS:
        for file_path in Path(directory).rglob(f"*{ext}"):
            try:
                docs = load_document(str(file_path))
                for doc in docs:
                    doc.metadata["source"] = str(file_path)
                all_docs.extend(docs)
            except Exception as e:
                print(f"Failed to load {file_path}: {e}")
    return all_docs
