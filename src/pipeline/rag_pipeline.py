from typing import List, Optional

from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough

from config import settings
from src.generation.llm import get_llm
from src.generation.prompt_templates import RAG_PROMPT
from src.ingestion.chunker import chunk_documents
from src.ingestion.embeddings import get_embedding_model
from src.ingestion.loader import load_document, load_documents_from_directory
from src.retrieval.retriever import format_documents, retrieve_documents
from src.retrieval.vector_store import add_documents, get_retriever, get_vector_store


def format_context(docs: List[Document]) -> str:
    return format_documents(docs)


class RAGPipeline:
    def __init__(self):
        self.embeddings = get_embedding_model()
        self.llm = get_llm()
        self._vector_store = None
        self._retriever = None

    def _ensure_retriever(self):
        if self._retriever is None:
            self._retriever = get_retriever(self.embeddings)
        return self._retriever

    def _ingest_and_setup(self, raw_docs: List[Document]):
        chunks = chunk_documents(raw_docs)
        self._vector_store = add_documents(chunks, self.embeddings)
        self._retriever = self._vector_store.as_retriever(
            search_kwargs={"k": settings.top_k}
        )
        print(f"Ingested {len(chunks)} chunks from {len(raw_docs)} documents.")

    def ingest_file(self, file_path: str):
        raw_docs = load_document(file_path)
        if not raw_docs:
            print("No documents found to ingest.")
            return
        self._ingest_and_setup(raw_docs)

    def ingest_directory(self, directory: str):
        raw_docs = load_documents_from_directory(directory)
        if not raw_docs:
            print("No documents found to ingest.")
            return
        self._ingest_and_setup(raw_docs)

    def query(self, question: str) -> str:
        retriever = self._ensure_retriever()
        docs = retrieve_documents(question, retriever)
        context = format_context(docs)

        chain = (
            RunnablePassthrough.assign(context=lambda _: context)
            | RAG_PROMPT
            | self.llm
        )
        response = chain.invoke({"question": question})
        return response.content
