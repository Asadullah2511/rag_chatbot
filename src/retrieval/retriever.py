from typing import List

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever


def retrieve_documents(
    query: str,
    retriever: VectorStoreRetriever,
) -> List[Document]:
    return retriever.invoke(query)


def format_documents(documents: List[Document]) -> str:
    formatted = []
    for i, doc in enumerate(documents, 1):
        source = doc.metadata.get("source", "Unknown")
        text = doc.page_content.strip()
        formatted.append(f"[Source {i}] ({source})\n{text}")
    return "\n\n---\n\n".join(formatted)
