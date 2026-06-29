import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.pipeline.rag_pipeline import RAGPipeline


def main():
    parser = argparse.ArgumentParser(description="Query the RAG system")
    parser.add_argument("question", type=str, help="Your question")
    args = parser.parse_args()

    pipeline = RAGPipeline()
    response = pipeline.query(args.question)
    print(response)


if __name__ == "__main__":
    main()
