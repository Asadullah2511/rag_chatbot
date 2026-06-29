from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

from config import settings


def get_embedding_model() -> Embeddings:
    if settings.llm_provider == "openai" and settings.openai_api_key:
        return OpenAIEmbeddings(
            model=settings.embedding_model,
            openai_api_key=settings.openai_api_key,
        )
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
