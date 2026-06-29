from typing import List, Optional

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStoreRetriever

from config import settings


def get_vector_store(
    embeddings: Embeddings,
    collection_name: Optional[str] = None,
) -> Chroma:
    return Chroma(
        collection_name=collection_name or settings.collection_name,
        embedding_function=embeddings,
        persist_directory=settings.persist_directory,
    )


def add_documents(
    documents: List[Document],
    embeddings: Embeddings,
    collection_name: Optional[str] = None,
) -> Chroma:
    vector_store = get_vector_store(embeddings, collection_name)
    vector_store.add_documents(documents)
    return vector_store


def get_retriever(
    embeddings: Embeddings,
    collection_name: Optional[str] = None,
    k: Optional[int] = None,
) -> VectorStoreRetriever:
    vector_store = get_vector_store(embeddings, collection_name)
    return vector_store.as_retriever(search_kwargs={"k": k or settings.top_k})
