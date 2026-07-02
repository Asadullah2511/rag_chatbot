import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import settings
from src.pipeline.rag_pipeline import RAGPipeline

app = FastAPI(title="DR Psychology - RAG API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = RAGPipeline()

PDF_PATH = Path(__file__).parent.parent / "notebooks" / "dark_pyscology.pdf"
if not Path(settings.persist_directory).exists():
    if PDF_PATH.exists():
        pipeline.ingest_file(str(PDF_PATH))


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    answer = pipeline.query(request.question)
    return QueryResponse(answer=answer)


@app.get("/health")
def health():
    return {"status": "ok"}
