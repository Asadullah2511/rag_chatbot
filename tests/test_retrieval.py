from src.retrieval.retriever import format_documents
from langchain_core.documents import Document


def test_format_documents():
    docs = [
        Document(page_content="Foo bar", metadata={"source": "a.txt"}),
        Document(page_content="Baz qux", metadata={"source": "b.txt"}),
    ]
    result = format_documents(docs)
    assert "[Source 1] (a.txt)" in result
    assert "[Source 2] (b.txt)" in result
    assert "Foo bar" in result
    assert "Baz qux" in result
