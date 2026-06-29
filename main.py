import sys
from pathlib import Path

from rich import print
from rich.panel import Panel

from src.pipeline.rag_pipeline import RAGPipeline


def main():
    pipeline = RAGPipeline()

    print(Panel.fit("[bold cyan]RAG Chatbot[/bold cyan]", border_style="cyan"))
    print("Commands: /ingest <dir> | /exit | type your question\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input == "/exit":
            print("Goodbye!")
            break

        if user_input.startswith("/ingest "):
            directory = user_input[len("/ingest "):].strip()
            if not Path(directory).exists():
                print(f"[red]Directory '{directory}' not found.[/red]")
                continue
            pipeline.ingest_directory(directory)
            continue

        response = pipeline.query(user_input)
        print(f"\n[bold green]Assistant:[/bold green] {response}\n")


if __name__ == "__main__":
    main()
