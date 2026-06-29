import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.pipeline.rag_pipeline import RAGPipeline


def main():
    parser = argparse.ArgumentParser(description="Ingest documents into the RAG vector store")
    parser.add_argument("directory", type=str, help="Path to directory containing documents")
    args = parser.parse_args()

    if not Path(args.directory).exists():
        print(f"Error: Directory '{args.directory}' does not exist.")
        sys.exit(1)

    pipeline = RAGPipeline()
    pipeline.ingest_directory(args.directory)


if __name__ == "__main__":
    main()
