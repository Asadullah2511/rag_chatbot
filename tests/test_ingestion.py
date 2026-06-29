import tempfile
from pathlib import Path

from src.ingestion.chunker import chunk_documents
from src.ingestion.loader import load_document, load_documents_from_directory


def test_load_text_file():
    with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", delete=False) as f:
        f.write("Hello world")
        f.flush()
        docs = load_document(f.name)
        assert len(docs) == 1
        assert "Hello world" in docs[0].page_content


def test_chunk_documents():
    from langchain_core.documents import Document

    docs = [Document(page_content="word " * 5000)]
    chunks = chunk_documents(docs)
    assert len(chunks) > 1
